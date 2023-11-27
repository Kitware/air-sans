import numpy as np

from . import mat_files as mf


class D11_Plus:
    Facility = "ILL"
    Instrument = "d11_plus"
    Name = "D11+_(2021-current)"
    Highlight = True
    # Filename
    filename_numeric_length = 6
    filename_lead_string = []
    filename_tail_string = []
    filename_extension_string = [".nxs"]
    filename_data_loader = "raw_read_ill_nexus_d11d22_2021"
    # Misc
    guide_size = [45e-3, 45e-3]  # [x,y]
    attenuators = [1, 112.8, 421.14, 1911.96]  # Attenautors 0, 1, 2, 3 etc.
    # Detector(s)
    detectors = 3
    # Main Panel
    detector1_type = "tube"
    detector1_view_position = "centre"
    detector1_name = "Main Panel"
    detector1_det_offset = 0  # position difference between panel and main detector
    detector1_pixels = [256, 192]  # Number of pixels, x,y
    detector1_pixel_size = [4, 8]
    # mm [x y]
    detector1_nominal_beam_centre = [128.5, 103.5]  # [x y]
    detector1_nominal_det_translation = [0, 0]  # mm [x y]
    detector1_dead_time = 1.5e-6 * np.ones(
        (192, 1)
    )  # the direction of this matrix determines the direction of the tubes
    detector1_imask_data = mf.read_mask_mat_file("./det_mask/det1_d11_plus.mat")
    detector1_relative_efficiency = (
        1  # Efficiency relative to rear detector (detector 1)
    )
    detector1_efficiency_data = mf.read_efficiency_mat_file_data(
        "./det_efficiency/det1_d11_plus.mat"
    )
    detector1_efficiency_error = mf.read_efficiency_mat_file_error(
        "./det_efficiency/det1_d11_plus.mat"
    )
    # Left Panel
    detector2_type = "tube"
    detector2_view_position = "left"
    detector2_name = "Left"
    detector2_det_offset = -0.105  # position difference between panel and main detector
    detector2_pixels = [32, 256]  # Number of pixels, x,y
    detector2_pixel_size = [8, 4]  # mm [x y]
    detector2_nominal_beam_centre = [16.5, 142.5]  # [x y]
    detector2_nominal_det_translation = [-628, 0]  # mm [x y]
    detector2_dead_time = 1.5e-6 * np.ones((1, 32))
    detector2_imask_data = mf.read_mask_mat_file("./det_mask/det2_d11_plus.mat")
    detector2_relative_efficiency = 1
    detector2_efficiency_data = mf.read_efficiency_mat_file_data(
        "./det_efficiency/det2_d11_plus.mat"
    )
    detector2_efficiency_error = mf.read_efficiency_mat_file_error(
        "./det_efficiency/det2_d11_plus.mat"
    )
    # Right Panel
    detector3_type = "tube"
    detector3_view_position = "right"
    detector3_name = "Right"
    detector3_det_offset = -0.105  # position difference between panel and main detector
    detector3_pixels = [32, 256]  # Number of pixels, x,y
    detector3_pixel_size = [8, 4]  # mm [x y]
    detector3_nominal_beam_centre = [16.5, 142.5]  # [x y]
    detector3_nominal_det_translation = [+628, 0]  # mm [x y]
    detector3_dead_time = 1.5e-6 * np.ones((1, 32))
    detector3_imask_data = mf.read_mask_mat_file("./det_mask/det3_d11_plus.mat")
    detector3_relative_efficiency = 1
    detector3_efficiency_data = mf.read_efficiency_mat_file_data(
        "./det_efficiency/det3_d11_plus.mat"
    )
    detector3_efficiency_error = mf.read_efficiency_mat_file_error(
        "./det_efficiency/det3_d11_plus.mat"
    )
