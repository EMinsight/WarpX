# Add tests (alphabetical order) ##############################################
#

add_warpx_test(
    test_3d_nodal_electrostatic_solver  # name
    3  # dims
    1  # nprocs
    inputs_test_3d_nodal_electrostatic_solver  # inputs
    analysis.py  # analysis
    diags/diag1000010  # output
    OFF  # dependency
)
label_warpx_test(test_3d_nodal_electrostatic_solver slow)
