# Add tests (alphabetical order) ##############################################
#

add_warpx_test(
    test_2d_particle_reflection_picmi  # name
    2  # dims
    1  # nprocs
    inputs_test_2d_particle_reflection_picmi.py  # inputs
    analysis_reflection.py  # analysis
    diags/diag1000010  # output
    OFF  # dependency
)

if(WarpX_EB)
    add_warpx_test(
        test_3d_particle_absorption  # name
        3  # dims
        2  # nprocs
        inputs_test_3d_particle_absorption  # inputs
        analysis_absorption.py  # analysis
        diags/diag1000060  # output
        OFF  # dependency
    )
endif()
