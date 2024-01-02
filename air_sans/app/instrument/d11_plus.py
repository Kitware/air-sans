import numpy as np
import h5py

from pathlib import Path
from . import mat_files as mf

BASE = Path(__file__).parent


class D11_Plus:
    def __init__(self):
        self.Facility = "ILL"
        self.Instrument = "D11+"
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
        self.reset_detector1_mask()
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
        self.reset_detector2_mask()
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
        self.reset_detector3_mask()
        self.detector3_relative_efficiency = 1
        self.detector3_efficiency_data = mf.read_efficiency_mat_file_data(
            BASE / "det_efficiency" / "det3_d11_plus.mat"
        )
        self.detector3_efficiency_error = mf.read_efficiency_mat_file_error(
            BASE / "det_efficiency" / "det3_d11_plus.mat"
        )

    def reset_detector1_mask(self):
        self.detector1_mask = np.where(
            self.detector1_imask_data == 1, np.nan, self.detector1_imask_data
        )

    def reset_detector2_mask(self):
        self.detector2_mask = np.where(
            self.detector2_imask_data == 1, np.nan, self.detector2_imask_data
        )

    def reset_detector3_mask(self):
        self.detector3_mask = np.where(
            self.detector3_imask_data == 1, np.nan, self.detector3_imask_data
        )

    def read_file(self, dir, path):
        self.path = dir + "/" + path
        root = h5py.File(self.path, "r")
        keys = list(root.keys())
        entry = root.name + keys[0]
        self.read_parameters(root, entry)

    def read_parameters(self, root, entry):
        # Run
        self.run_number = self.read_value(root, entry, "/run_number")
        self.user = self.read_value(root, entry, "/user/name")
        self.start_time = self.read_value(root, entry, "/start_time")
        self.end_time = self.read_value(root, entry, "/end_time")
        self.duration = self.read_value(root, entry, "/duration")
        self.experiment_identifier = self.read_value(
            root, entry, "/experiment_identifier"
        )
        self.experiment_title = self.read_value(root, entry, "/experiment_title")
        self.sample_description = self.read_value(root, entry, "/sample_description")
        # Detector Distance & Motors
        self.pixel1_y = self.read_value(root, entry, "/D11/Detector 1/pixel_size_y")
        self.pixel1_x = self.read_value(root, entry, "/D11/Detector 1/pixel_size_x")
        # Detector rate
        self.det1_rate = self.read_value(root, entry, "/D11/Detector 1/det1_rate")
        # Detector motors
        self.det1_actual = self.read_value(
            root,
            entry,
            "/D11/Detector 1/det1_actual",
            fallback_item="/D11/Detector 1/det_actual",
        )
        self.det1_calc = self.read_value(
            root,
            entry,
            "/D11/Detector 1/det1_calc",
            fallback_item="/D11/Detector 1/det_calc",
        )
        self.dan1_actual = self.read_value(
            root,
            entry,
            "/D11/Detector 1/dan1_actual",
            fallback_item="/D11/Detector 1/dan_actual",
        )
        self.dtr1_actual = self.read_value(
            root,
            entry,
            "/D11/Detector 1/dtr1_actual",
            fallback_item="/D11/Detector 1/dtr_actual",
        )
        # BeamStop
        self.bx1_actual = self.read_value(
            root,
            entry,
            "/D11//beamstop/bx1_actual",
            fallback_item="/D11//beamstop/bx_actual",
            default=0.0,
        )
        self.by1_actual = self.read_value(
            root,
            entry,
            "/D11//beamstop/by1_actual",
            fallback_item="/D11//beamstop/by_actual",
            default=0.0,
        )

        self.pixel2_y = self.read_value(root, entry, "/D11/Detector 2/pixel_size_y")
        self.pixel2_x = self.read_value(root, entry, "/D11/Detector 2/pixel_size_x")
        # Detector rate
        self.det2_rate = self.read_value(root, entry, "/D11/Detector 2/det2_rate")
        # Detector motors
        self.det2_actual = self.read_value(
            root,
            entry,
            "/D11/Detector 2/det2_actual",
            fallback_item="/D11/Detector 2/det_actual",
        )
        self.det2_calc = self.read_value(
            root,
            entry,
            "/D11/Detector 2/det2_calc",
            fallback_item="/D11/Detector 2/det_calc",
        )
        self.dan2_actual = self.read_value(
            root,
            entry,
            "/D11/Detector 2/dan2_actual",
            fallback_item="/D11/Detector 2/dan_actual",
        )
        self.dtr2_actual = self.read_value(
            root,
            entry,
            "/D11/Detector 2/dtr2_actual",
            fallback_item="/D11/Detector 2/dtr_actual",
        )
        # BeamStop
        self.bx2_actual = self.read_value(
            root,
            entry,
            "/D11//beamstop/bx2_actual",
            fallback_item="/D11//beamstop/bx_actual",
            default=0.0,
        )
        self.by2_actual = self.read_value(
            root,
            entry,
            "/D11//beamstop/by2_actual",
            fallback_item="/D11//beamstop/by_actual",
            default=0.0,
        )

        self.pixel3_y = self.read_value(root, entry, "/D11/Detector 3/pixel_size_y")
        self.pixel3_x = self.read_value(root, entry, "/D11/Detector 3/pixel_size_x")
        # Detector rate
        self.det3_rate = self.read_value(root, entry, "/D11/Detector 3/det3_rate")
        # Detector motors
        self.det3_actual = self.read_value(
            root,
            entry,
            "/D11/Detector 3/det3_actual",
            fallback_item="/D11/Detector 3/det_actual",
        )
        self.det3_calc = self.read_value(
            root,
            entry,
            "/D11/Detector 3/det3_calc",
            fallback_item="/D11/Detector 3/det_calc",
        )
        self.dan3_actual = self.read_value(
            root,
            entry,
            "/D11/Detector 3/dan3_actual",
            fallback_item="/D11/Detector 3/dan_actual",
        )
        self.dtr3_actual = self.read_value(
            root,
            entry,
            "/D11/Detector 3/dtr3_actual",
            fallback_item="/D11/Detector 3/dtr_actual",
        )
        # BeamStop
        self.bx3_actual = self.read_value(
            root,
            entry,
            "/D11//beamstop/bx3_actual",
            fallback_item="/D11//beamstop/bx_actual",
            default=0.0,
        )
        self.by3_actual = self.read_value(
            root,
            entry,
            "/D11//beamstop/by3_actual",
            fallback_item="/D11//beamstop/by_actual",
            default=0.0,
        )
        # Wavelength
        self.wavelength = self.read_value(root, entry, "/D11/selector/wavelength")
        self.wavelength_res = (
            self.read_value(root, entry, "/D11/selector/wavelength_res", default=10)
            / 100
        )
        self.rotation_speed = self.read_value(
            root, entry, item="/D11/selector/rotation_speed"
        )
        self.seltrs_actual = self.read_value(root, entry, "/D11/selector/seltrs_actual")

        # Attenuator
        self.attenuator_position = self.read_value(
            root, entry, "/D11/attenuator/position", default=0
        )
        self.attenuation_coefficient = self.read_value(
            root, entry, "/D11/attenuator/attenuation_coefficient"
        )
        self.attenuation_value = self.read_value(
            root,
            entry,
            "/D11/attenuator/attenuation_value",
            default=[
                self.attenuators[1],
                self.attenuators[2],
                self.attenuators[3],
            ],
        )
        # Collimation
        self.collimation_actual_position = self.read_value(
            root, entry, "/D11/collimation/actual_position"
        )
        # Source Size
        temp = self.read_array(
            root,
            entry,
            "/D11/collimation/ap_size",
            default=[self.guide_size[0] * 1000, self.guide_size[1] * 1000],
        )
        self.collimation_ap_size_x = temp[0] / 1000
        self.collimation_ap_size_y = temp[1] / 1000
        # Reactor Power
        self.reactor_power = self.read_value(root, entry, "/reactor_power")
        # Sample
        self.sample_thickness = self.read_value(root, entry, "/sample/thickness")
        # Sample Motors
        self.sample_san_actual = self.read_value(root, entry, "/sample/san_actual")
        self.sample_phi_actual = self.read_value(root, entry, "/sample/phi_actual")
        self.sample_sdi1_actual = self.read_value(root, entry, "/sample/sdi1_actual")
        self.sample_sdi_actual = self.read_value(root, entry, "/sample/sdi_actual")
        self.sample_sdi2_actual = self.read_value(root, entry, "/sample/sdi2_actual")
        self.sample_trs_actual = self.read_value(root, entry, "/sample/trs_actual")
        self.sample_sht_actual = self.read_value(root, entry, "/sample/sht_actual")
        self.sample_str_actual = self.read_value(root, entry, "/sample/str_actual")
        self.sample_changer_value = self.read_value(
            root, entry, "/sample/sample_changer_value"
        )
        self.sample_omega_actual = self.read_value(root, entry, "/sample/omega_actual")
        self.sample_TrMicro_actual = self.read_value(
            root, entry, "/sample/TrMicro_actual"
        )
        self.sample_TrMicro_offset = self.read_value(
            root, entry, "/sample/TrMicro_offset"
        )
        self.sample_TrMicro_requested = self.read_value(
            root, entry, "/sample/TrMicro_requested"
        )

        # Sample environment
        self.sample_temperature = self.read_value(root, entry, "/sample/temperature")
        self.sample_regulation_temperature = self.read_value(
            root, entry, "/sample/regulation_temperature"
        )
        self.sample_setpoint_temperature = self.read_value(
            root, entry, "/sample/setpoint_temperature"
        )
        self.sample_bath1_regulation_temperature = self.read_value(
            root, entry, "/sample/bath1_regulation_temperature"
        )
        self.sample_bath1_setpoint_temperature = self.read_value(
            root, entry, "/sample/bath1_setpoint_temperature"
        )
        self.sample_bath2_regulation_temperature = self.read_value(
            root, entry, "/sample/bath2_regulation_temperature"
        )
        self.sample_bath2_setpoint_temperature = self.read_value(
            root, entry, "/sample/bath2_setpoint_temperature"
        )
        self.sample_bath_selector_actual = self.read_value(
            root, entry, "/sample/bath_selector_actual"
        )
        self.sample_air_temperature = self.read_value(
            root, entry, "/sample/air_temperature"
        )
        self.sample_rack_temperature = self.read_value(
            root, entry, "/sample/rack_temperature"
        )

        # Power Supplies
        self.sample_ps1_current = self.read_value(root, entry, "/sample/ps1_current")
        self.sample_ps1_voltage = self.read_value(root, entry, "/sample/ps1_voltage")
        self.sample_ps2_current = self.read_value(root, entry, "/sample/ps2_current")
        self.sample_ps2_voltage = self.read_value(root, entry, "/sample/ps2_voltage")
        self.sample_ps3_current = self.read_value(root, entry, "/sample/ps3_current")
        self.sample_ps3_voltage = self.read_value(root, entry, "/sample/ps3_voltage")

        # Magnet
        self.sample_field_actual = self.read_value(root, entry, "/sample/field_actual")

        # Shear
        self.sample_shearrate_actual = self.read_value(
            root, entry, "/sample/shearrate_actual"
        )

        # Read Detector Data, Monitor and Time Slices
        self.detector_detsum = self.read_value(root, entry, "/detector/detsum")
        self.detector_detrate = self.read_value(root, entry, "/detector/detrate")

        # Determine Measurement Mode, Single, Kinetic or TOF
        self.mode = int(self.read_value(root, entry, "/mode", default=0))
        if self.mode == 0:
            self.file_type = "mono"
        elif self.mode == 1:
            self.file_type = "tof"
            tof_params = self.read_value(root, entry, "/monitor1/time_of_flight")
            if tof_params is not None:
                self.tof_width = tof_params[0]
                self.tof_channels = tof_params[1]
                self.tof_delay = tof_params[2]
                self.pickups = self.read_value(root, entry, "/monitor1/nbpickup")
                self.tof_period = (self.tof_width * self.tof_channels) + self.tof_delay
                self.tof_mode = self.read_value(root, entry, "/tof/tof_mode", default=0)
        elif self.mode == 3:
            self.file_type = "kinetic"
            self.slices = self.read_value(root, entry, "/slices")
            if self.slices is not None:
                # time lapse of the first frame - added to below with subsequent frames
                self.frame_time = self.slices[0] / 2
                self.pickups = self.read_value(root, entry, "/nbrepaint")
        elif self.mode == 4:
            self.file_type = "tof_inelastic"
            tof_params = self.read_value(root, entry, "/monitor1/time_of_flight")
            if tof_params is not None:
                self.tof_width = tof_params[0]
                self.tof_channels = tof_params[1]
                self.tof_delay = tof_params[2]
                self.pickups = self.read_value(root, entry, "/monitor1/nbpickup")
                self.tof_period = (self.tof_width * self.tof_channels) + self.tof_delay
        else:
            self.file_type = "unknown"

        # Detector Distance & Motors

        det = self.read_array(
            root, entry, "/D11/Detector 1/data1", fallback_item="/D11/Detector 1/data"
        )
        det_size = det.shape
        if len(det_size) < 3:
            det_size[2] = 1
        if self.file_type == "mono":
            det = det.reshape([det_size[2], det_size[0], det_size[1]])
            self.n_frames = det_size[2]
            self.det1_data = det[0, :, :].transpose()
            self.nx1, self.ny1 = self.det1_data.shape
        if self.file_type == "kinetic":
            if len(det_size) == 4:
                det = det.reshape(det_size[0], det_size[2], det_size[3])
            else:
                det = det.reshape(det_size[0], det_size[1], det_size[2])
            self.n_frames = det_size[0]
            self.det1_data = det[0, :, :].transpose()
            self.nx1, self.ny1 = self.det1_data.shape
            self.duration = self.duration / self.n_frames
        if self.file_type == "tof":
            det = det.reshape(det_size[0], det_size[1], det_size[2])
            self.det1_data = det[0, :, :].transpose()
            self.nx1, self.ny1 = self.det1_data.shape
            self.n_frames = det_size[0]
            self.duration = self.duration / self.n_frames
            # read tof wavelengths
            try:
                self.tof_wavs1 = self.read_value(
                    root, entry, "/tof/tof_wavelength_detector1"
                )
                self.tof_res1 = np.ones(self.n_frames)
            except Exception:
                self.tof_wavs1 = np.arrange(self.tof_channels)
                self.tof_res1 = np.ones(self.tof_channels)
        if self.file_type == "tof_inelastic":
            det = det.reshape(det_size[0], det_size[1], det_size[2])
            self.det1_data = det[0, :, :].transpose()
            self.nx1, self.ny1 = self.det1_data.shape
            self.n_frames = det_size[0]
            self.duration = self.duration / self.n_frames
            # read tof wavelengths
            try:
                self.tof_wavs1 = self.read_value(
                    root, entry, "/tof/tof_wavelength_detector1"
                )
                self.tof_res1 = np.ones(self.n_frames)
            except Exception:
                self.tof_wavs1 = np.ones(self.n_frames) * self.wavelength
                self.tof_res1 = np.ones(self.n_frames) * self.wavelength_res

        det = self.read_array(
            root, entry, "/D11/Detector 2/data2", fallback_item="/D11/Detector 2/data"
        )
        det_size = det.shape
        if len(det_size) < 3:
            det_size[2] = 1
        if self.file_type == "mono":
            det = det.reshape([det_size[2], det_size[0], det_size[1]])
            self.n_frames = det_size[2]
            self.det2_data = det[0, :, :].transpose()
            self.nx2, self.ny2 = self.det2_data.shape
        if self.file_type == "kinetic":
            if len(det_size) == 4:
                det = det.reshape(det_size[0], det_size[2], det_size[3])
            else:
                det = det.reshape(det_size[0], det_size[1], det_size[2])
            self.n_frames = det_size[0]
            self.det2_data = det[0, :, :].transpose()
            self.nx2, self.ny2 = self.det2_data.shape
            self.duration = self.duration / self.n_frames
        if self.file_type == "tof":
            det = det.reshape(det_size[0], det_size[1], det_size[2])
            self.det2_data = det[0, :, :].transpose()
            self.nx2, self.ny2 = self.det2_data.shape
            self.n_frames = det_size[0]
            self.duration = self.duration / self.n_frames
            # read tof wavelengths
            try:
                self.tof_wavs2 = self.read_value(
                    root, entry, "/tof/tof_wavelength_detector1"
                )
                self.tof_res2 = np.ones(self.n_frames)
            except Exception:
                self.tof_wavs2 = np.arrange(self.tof_channels)
                self.tof_res2 = np.ones(self.tof_channels)
        if self.file_type == "tof_inelastic":
            det = det.reshape(det_size[0], det_size[1], det_size[2])
            self.det2_data = det[0, :, :].transpose()
            self.nx2, self.ny2 = self.det2_data.shape
            self.n_frames = det_size[0]
            self.duration = self.duration / self.n_frames
            # read tof wavelengths
            try:
                self.tof_wavs2 = self.read_value(
                    root, entry, "/tof/tof_wavelength_detector1"
                )
                self.tof_res2 = np.ones(self.n_frames)
            except Exception:
                self.tof_wavs2 = np.ones(self.n_frames) * self.wavelength
                self.tof_res2 = np.ones(self.n_frames) * self.wavelength_res

        det = self.read_array(
            root, entry, "/D11/Detector 3/data3", fallback_item="/D11/Detector 3/data"
        )
        det_size = det.shape
        if len(det_size) < 3:
            det_size[2] = 1
        if self.file_type == "mono":
            det = det.reshape([det_size[2], det_size[0], det_size[1]])
            self.n_frames = det_size[2]
            self.det3_data = det[0, :, :].transpose()
            self.nx3, self.ny3 = self.det3_data.shape
        if self.file_type == "kinetic":
            if len(det_size) == 4:
                det = det.reshape(det_size[0], det_size[2], det_size[3])
            else:
                det = det.reshape(det_size[0], det_size[1], det_size[2])
            self.n_frames = det_size[0]
            self.det3_data = det[0, :, :].transpose()
            self.nx3, self.ny3 = self.det3_data.shape
            self.duration = self.duration / self.n_frames
        if self.file_type == "tof":
            det = det.reshape(det_size[0], det_size[1], det_size[2])
            self.det3_data = det[0, :, :].transpose()
            self.nx3, self.ny3 = self.det3_data.shape
            self.n_frames = det_size[0]
            self.duration = self.duration / self.n_frames
            # read tof wavelengths
            try:
                self.tof_wavs3 = self.read_value(
                    root, entry, "/tof/tof_wavelength_detector1"
                )
                self.tof_res3 = np.ones(self.n_frames)
            except Exception:
                self.tof_wavs3 = np.arrange(self.tof_channels)
                self.tof_res3 = np.ones(self.tof_channels)
        if self.file_type == "tof_inelastic":
            det = det.reshape(det_size[0], det_size[1], det_size[2])
            self.det3_data = det[0, :, :].transpose()
            self.nx3, self.ny3 = self.det3_data.shape
            self.n_frames = det_size[0]
            self.duration = self.duration / self.n_frames
            # read tof wavelengths
            try:
                self.tof_wavs3 = self.read_value(
                    root, entry, "/tof/tof_wavelength_detector1"
                )
                self.tof_res3 = np.ones(self.n_frames)
            except Exception:
                self.tof_wavs3 = np.ones(self.n_frames) * self.wavelength
                self.tof_res3 = np.ones(self.n_frames) * self.wavelength_res
        # Read Monitor Data - all frames
        self.monitor1_data = self.read_array(root, entry, "/monitor1/data", default=1)

    def read_value(self, root, entry, item, fallback_item=None, default=None):
        try:
            temp = root[entry + item]
            value = temp[0]
        except Exception:
            if fallback_item is not None:
                try:
                    temp = root[entry + fallback_item]
                    value = temp[0]
                except Exception:
                    # print("Bad file - Bad Fallback", item, fallback_item)
                    return default
            else:
                # print("Bad file - default", item, default)
                return default
        return value

    def read_array(self, root, entry, item, fallback_item=None, default=None):
        try:
            temp = root[entry + item]
            value = temp[()]
        except Exception:
            if fallback_item is not None:
                try:
                    temp = root[entry + fallback_item]
                    value = temp[()]
                except Exception:
                    # print("Bad file - Bad Fallback", item, fallback_item)
                    return default
            else:
                # print("Bad file - default", item, default)
                return default
        return value
