# Add tests (alphabetical order) ##############################################
#

add_warpx_test(
    test_3d_flux_injection  # name
    3  # dims
    2  # nprocs
    inputs_test_3d_flux_injection  # inputs
    analysis_flux_injection_3d.py  # analysis
    diags/diag1000002  # output
    OFF  # dependency
)

add_warpx_test(
    test_rz_flux_injection  # name
    RZ  # dims
    2  # nprocs
    inputs_test_rz_flux_injection  # inputs
    analysis_flux_injection_rz.py  # analysis
    diags/diag1000120  # output
    OFF  # dependency
)
