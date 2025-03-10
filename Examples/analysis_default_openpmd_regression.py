#!/usr/bin/env python3

import os
import re
import sys

sys.path.insert(1, "../../../../warpx/Regression/Checksum/")
import checksumAPI

# this will be the name of the plot file
fn = sys.argv[1]

# Get name of the test
test_name = os.path.split(os.getcwd())[1]

# Run checksum regression test
if re.search("single_precision", fn):
    checksumAPI.evaluate_checksum(test_name, fn, output_format="openpmd", rtol=2.0e-6)
else:
    checksumAPI.evaluate_checksum(test_name, fn, output_format="openpmd")
