#!/usr/bin/env python3

# Copyright 2019-2020 Luca Fedeli, Maxence Thevenet
#
# This file is part of WarpX.
#
# License: BSD-3-Clause-LBNL


"""
This script tests the result of the ionization module in WarpX.

Input files inputs.rt and inputs.bf.rt are used to reproduce the test from
Chen, JCP, 2013, figure 2 (in the lab frame and in a boosted frame,
respectively): a plane-wave laser pulse propagates through a
uniform N2+ neutral plasma and further ionizes the Nitrogen atoms. This test
checks that, after the laser went through the plasma, ~32% of Nitrogen
ions are N5+, in agreement with theory from Chen's article.
"""

import os
import sys

import numpy as np
import yt

yt.funcs.mylog.setLevel(0)
sys.path.insert(1, "../../../../warpx/Regression/Checksum/")
import checksumAPI

# Open plotfile specified in command line, and get ion's ionization level.
filename = sys.argv[1]
ds = yt.load(filename)
ad = ds.all_data()
ilev = ad["ions", "particle_ionizationLevel"].v

# Fraction of Nitrogen ions that are N5+.
N5_fraction = ilev[ilev == 5].size / float(ilev.size)

print("Number of ions: " + str(ilev.size))
print("Number of N5+ : " + str(ilev[ilev == 5].size))
print("N5_fraction   : " + str(N5_fraction))

do_plot = False
if do_plot:
    import matplotlib.pyplot as plt

    all_data_level_0 = ds.covering_grid(
        level=0, left_edge=ds.domain_left_edge, dims=ds.domain_dimensions
    )
    F = all_data_level_0["boxlib", "Ex"].v.squeeze()
    extent = [
        ds.domain_left_edge[1],
        ds.domain_right_edge[1],
        ds.domain_left_edge[0],
        ds.domain_right_edge[0],
    ]
    ad = ds.all_data()

    # Plot ions with ionization levels
    species = "ions"
    xi = ad[species, "particle_position_x"].v
    zi = ad[species, "particle_position_y"].v
    ii = ad[species, "particle_ionizationLevel"].v
    plt.figure(figsize=(10, 10))
    plt.subplot(211)
    plt.imshow(np.abs(F), extent=extent, aspect="auto", cmap="magma", origin="default")
    plt.colorbar()
    for lev in range(int(np.max(ii) + 1)):
        select = ii == lev
        plt.scatter(
            zi[select], xi[select], s=0.2, label="ionization level: " + str(lev)
        )
    plt.legend()
    plt.title("abs(Ex) (V/m) and ions")
    plt.xlabel("z (m)")
    plt.ylabel("x (m)")
    plt.subplot(212)
    plt.imshow(np.abs(F), extent=extent, aspect="auto", cmap="magma", origin="default")
    plt.colorbar()

    # Plot electrons
    species = "electrons"
    if species in [x[0] for x in ds.field_list]:
        xe = ad[species, "particle_position_x"].v
        ze = ad[species, "particle_position_y"].v
        plt.scatter(ze, xe, s=0.1, c="r", label="electrons")
    plt.title("abs(Ex) (V/m) and electrons")
    plt.xlabel("z (m)")
    plt.ylabel("x (m)")
    plt.savefig("image_ionization.pdf", bbox_inches="tight")

error_rel = abs(N5_fraction - 0.32) / 0.32
tolerance_rel = 0.07

print("error_rel    : " + str(error_rel))
print("tolerance_rel: " + str(tolerance_rel))

assert error_rel < tolerance_rel

# Check that the user runtime component (if it exists) worked as expected
try:
    orig_z = ad["electrons", "particle_orig_z"].v
    print(f"orig_z: min = {np.min(orig_z)}, max = {np.max(orig_z)}")
    assert np.all((orig_z > 0.0) & (orig_z < 1.5e-5))
    print("particle_orig_z has reasonable values")
except yt.utilities.exceptions.YTFieldNotFound:
    pass  # The backtransformed diagnostic version of the test does not have orig_z

test_name = os.path.split(os.getcwd())[1]
checksumAPI.evaluate_checksum(test_name, filename)
