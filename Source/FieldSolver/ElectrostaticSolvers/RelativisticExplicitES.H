
/* Copyright 2024 The WarpX Community
 *
 * This file is part of WarpX.
 *
 * Authors: Remi Lehe, Roelof Groenewald, Arianna Formenti, Revathi Jambunathan
 *
 * License: BSD-3-Clause-LBNL
 */
#ifndef WARPX_RELATIVISTICEXPLICITES_H_
#define WARPX_RELATIVISTICEXPLICITES_H_

#include "ElectrostaticSolver.H"
#include "Particles/WarpXParticleContainer.H"


class RelativisticExplicitES final : public ElectrostaticSolver
{
public:

    RelativisticExplicitES (int nlevs_max) : ElectrostaticSolver (nlevs_max) {
        ReadParameters();
    }

    void InitData () override;

    /**
     * \brief Computes electrostatic fields for species
     * that have initialize self fields turned on.
     * A loop over all the species is performed and for each species (with self fields)
     * the function ``AddSpaceChargeField`` is called.
     * This function computes the electrostatic potential for species charge denisyt as source
     * and then the electric and magnetic fields are updated to include the
     * corresponding fields from the electrostatic potential.
     * Then electric and magnetic fields are updated to include potential variation
     * due to boundary conditions using the function ``AddBoundaryField``
     *
     * \param[in,unused] rho_fp A temporary multifab is used for species charge density
     * \param[in,unused] rho_cp A temporary multifab is used to store species charge density on coarse patch
     * \param[in] charge_buf Buffer region to synchronize charge density from fine and coarse patch
     * \param[in,unused] phi_fp A temporary multifab is used to compute electrostatic potentail for each species
     * \param[in] mpc Pointer to multi particle container to access species data
     * \param[in,out] Efield_fp Field contribution from phi computed from each species' charge density is added
     * \param[in,out] Bfield Field contribution from phi computed from each species' charge density is added
     */
    void ComputeSpaceChargeField (
        [[maybe_unused]] amrex::Vector< std::unique_ptr<amrex::MultiFab> >& rho_fp,
        [[maybe_unused]] amrex::Vector< std::unique_ptr<amrex::MultiFab> >& rho_cp,
                         amrex::Vector< std::unique_ptr<amrex::MultiFab> >& charge_buf,
                         amrex::Vector< std::unique_ptr<amrex::MultiFab> >& phi_fp,
                         MultiParticleContainer& mpc,
        [[maybe_unused]] MultiFluidContainer* mfl,
                         amrex::Vector< std::array< std::unique_ptr<amrex::MultiFab>, 3> >& Efield_fp,
                         amrex::Vector< std::array< std::unique_ptr<amrex::MultiFab>, 3> >& Bfield_fp
    ) override;

    /**
     * Compute the charge density of the species paricle container, pc,
     * and obtain the corresponding electrostatic potential to
     * update the electric and magnetic fields.
     * \param[in] charge_buf Multifab that stores buffer region to
     *                       synchronize charge density on fine and coarse patch
     * \param[in] pc particle container for the selected species
     * \param[in] Efield Efield updated to include potential computed for selected species charge density as source
     * \param[in] Bfield Bfield updated to include potential computed for selected species charge density as source
     */
    void AddSpaceChargeField (
        amrex::Vector<std::unique_ptr<amrex::MultiFab> >& charge_buf,
        WarpXParticleContainer& pc,
        amrex::Vector<std::array< std::unique_ptr<amrex::MultiFab>, 3>>& Efield,
        amrex::Vector<std::array< std::unique_ptr<amrex::MultiFab>, 3>>& Bfield
    );

    /** Compute the potential `phi` by solving the Poisson equation with the
       simulation specific boundary conditions and boundary values, then add the
       E field due to that `phi` to `Efield_fp`.
    * \param[in] Efield Efield updated to include potential gradient from boundary condition
    */
    void AddBoundaryField (
        amrex::Vector<std::array< std::unique_ptr<amrex::MultiFab>, 3>>& Efield
    );
};

#endif // WARPX_RELATIVISTICEXPLICITES_H_
