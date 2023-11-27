import numpy as np

from pathlib import Path
from . import mat_files as mf

BASE = Path(__file__).parent


class D11_Plus:
    def __init__(self):
        self.Facility = "ILL"
        self.Instrument = "d11_plus"
        self.Name = "D11+_(2021-current)"
        self.Highlight = True
        # Filename
        self.filename_numeric_length = 6
        self.filename_lead_string = []
        self.filename_tail_string = []
        self.filename_extension_string = [".nxs"]
        self.filename_data_loader = "raw_read_ill_nexus_d11d22_2021"
        # Misc
        self.guide_size = [45e-3, 45e-3]  # [x,y]
        self.attenuators = [1, 112.8, 421.14, 1911.96]  # Attenautors 0, 1, 2, 3 etc.
        # Detector(s)
        self.detectors = 3
        # Main Panel
        self.detector1_type = "tube"
        self.detector1_view_position = "centre"
        self.detector1_name = "Main Panel"
        self.detector1_det_offset = (
            0  # position difference between panel and main detector
        )
        self.detector1_pixels = [256, 192]  # Number of pixels, x,y
        self.detector1_pixel_size = [4, 8]
        # mm [x y]
        self.detector1_nominal_beam_centre = [128.5, 103.5]  # [x y]
        self.detector1_nominal_det_translation = [0, 0]  # mm [x y]
        self.detector1_dead_time = 1.5e-6 * np.ones(
            (192, 1)
        )  # the direction of this matrix determines the direction of the tubes
        self.detector1_imask_data = mf.read_mask_mat_file(
            BASE / "det_mask" / "det1_d11_plus.mat"
        )
        self.detector1_relative_efficiency = (
            1  # Efficiency relative to rear detector (detector 1)
        )
        self.detector1_efficiency_data = mf.read_efficiency_mat_file_data(
            BASE / "det_efficiency" / "det1_d11_plus.mat"
        )
        self.detector1_efficiency_error = mf.read_efficiency_mat_file_error(
            BASE / "det_efficiency" / "det1_d11_plus.mat"
        )
        # Left Panel
        self.detector2_type = "tube"
        self.detector2_view_position = "left"
        self.detector2_name = "Left"
        self.detector2_det_offset = (
            -0.105
        )  # position difference between panel and main detector
        self.detector2_pixels = [32, 256]  # Number of pixels, x,y
        self.detector2_pixel_size = [8, 4]  # mm [x y]
        self.detector2_nominal_beam_centre = [16.5, 142.5]  # [x y]
        self.detector2_nominal_det_translation = [-628, 0]  # mm [x y]
        self.detector2_dead_time = 1.5e-6 * np.ones((1, 32))
        self.detector2_imask_data = mf.read_mask_mat_file(
            BASE / "det_mask" / "det2_d11_plus.mat"
        )
        self.detector2_relative_efficiency = 1
        self.detector2_efficiency_data = mf.read_efficiency_mat_file_data(
            BASE / "det_efficiency" / "det2_d11_plus.mat"
        )
        self.detector2_efficiency_error = mf.read_efficiency_mat_file_error(
            BASE / "det_efficiency" / "det2_d11_plus.mat"
        )
        # Right Panel
        self.detector3_type = "tube"
        self.detector3_view_position = "right"
        self.detector3_name = "Right"
        self.detector3_det_offset = (
            -0.105
        )  # position difference between panel and main detector
        self.detector3_pixels = [32, 256]  # Number of pixels, x,y
        self.detector3_pixel_size = [8, 4]  # mm [x y]
        self.detector3_nominal_beam_centre = [16.5, 142.5]  # [x y]
        self.detector3_nominal_det_translation = [+628, 0]  # mm [x y]
        self.detector3_dead_time = 1.5e-6 * np.ones((1, 32))
        self.detector3_imask_data = mf.read_mask_mat_file(
            BASE / "det_mask" / "det3_d11_plus.mat"
        )
        self.detector3_relative_efficiency = 1
        self.detector3_efficiency_data = mf.read_efficiency_mat_file_data(
            BASE / "det_efficiency" / "det3_d11_plus.mat"
        )
        self.detector3_efficiency_error = mf.read_efficiency_mat_file_error(
            BASE / "det_efficiency" / "det3_d11_plus.mat"
        )
