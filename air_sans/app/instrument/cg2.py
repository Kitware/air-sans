import numpy as np
import xmltodict

from pathlib import Path

BASE = Path(__file__).parent


class CG2:
    def __init__(self):
        self.Facility = "ORNL"
        self.Instrument = "CG2"
        # Filename
        self.filename_numeric_length = 4
        self.filename_lead_string = "xxxxxxxxx"
        self.filename_tail_string = []
        self.filename_extension_string = [".xml"]
        self.filename_data_loader = "raw_read_ornl_sans"
        # Misc
        self.guide_size = [40e-3, 40e-3]  # [x,y]
        self.attenuators = [
            1,
            3.605,
            43.85,
            553.544,
            3456,
            22973.37,
            69043,
        ]  # Attenautors 0, 1, 2, 3 etc.
        # Detector(s)
        self.detectors = 1
        # Main Panel
        self.detector1_type = "tube"
        self.detector1_view_position = "centre"
        self.detector1_name = "Rear"
        self.detector1_nominal_det_translation = [0, 0]
        self.detector1_dead_time = 0.6 * 10e-6
        self.detector1_pixels = [192, 256]
        self.detector1_pixel_size = [5.5, 3.94]  # mm [x y]
        self.detector1_nominal_beam_centre = [96.5, 128.5]  # [x,y]
        self.detector1_imask_file = "ornl_cg2_msk.msk"
        self.detector1_mask = np.empty((256, 192)) * np.nan
        self.detector1_relative_efficiency = 1
        self.detector1_efficiency_file = ""
        self.detector1_efficiency_data = np.ones((256, 192))
        self.detector1_efficiency_error = np.zeros((256, 192))

    def read_file(self, dir, path):
        self.path = dir + "/" + path
        with open(self.path) as fd:
            root = xmltodict.parse(fd.read(), process_namespaces=True)
        # print(root['SPICErack'].keys())
        self.SPICE_version = self.read_value(root["SPICErack"], "@SPICE_version")
        self.read_parameters(root["SPICErack"])

    def read_parameters(self, root):
        # Header
        self.Instrument = self.read_value(root["Header"], "Instrument")
        temp = self.read_value(root["Header"], "Start_Time")
        if temp is not None:
            self.Start_Date = temp[0:10]
            self.Start_Time = temp[-8:]
        temp = self.read_value(root["Header"], "End_Time")
        if temp is not None:
            self.End_Date = temp[0:10]
            self.End_Time = temp[-8:]
        self.Reactor_Power = self.read_typed_value(root["Header"], "Reactor_Power")
        self.Experiment_Title = self.read_value(root["Header"], "Experiment_Title")
        self.Experiment_number = self.read_typed_value(
            root["Header"], "Experiment_number"
        )
        self.IPTS_number = self.read_value(root["Header"], "IPTS_number")
        self.Cycle_Number = self.read_value(root["Header"], "Cycle_Number")
        self.Command = self.read_value(root["Header"], "Command")
        self.Users = self.read_value(root["Header"], "Users")
        self.Local_Contact = self.read_value(root["Header"], "Local_Contact")
        self.Scan_Number = self.read_typed_value(root["Header"], "Scan_Number")
        self.Scan_Point_Number = self.read_typed_value(
            root["Header"], "Scan_Point_Number"
        )
        self.Scan_Title = self.read_value(root["Header"], "Scan_Title")
        self.Sample_Name = self.read_value(root["Header"], "Sample_Name")
        self.Sample_ID = self.read_value(root["Header"], "Sample_ID")
        self.Sample_Changer = self.read_value(root["Header"], "Sample_Changer")
        self.Sample_Changer_Position = self.read_typed_value(
            root["Header"], "Sample_Changer_Position"
        )
        self.Sample_Thickness = self.read_typed_value(
            root["Header"], "Sample_Thickness"
        )
        self.Sample_CountRate = self.read_typed_value(
            root["Header"], "Sample_CountRate"
        )
        self.Transmission = self.read_value(root["Header"], "Transmission")
        self.Scan_Type = self.read_value(root["Header"], "Scan_Type")
        self.Sample_Type = self.read_value(root["Header"], "Sample_Type")
        self.Number_of_X_Pixels = self.read_typed_value(
            root["Header"], "Number_of_X_Pixels"
        )
        self.Number_of_Y_Pixels = self.read_typed_value(
            root["Header"], "Number_of_Y_Pixels"
        )
        self.west_wing_number_of_x_Pixels = self.read_typed_value(
            root["Header"], "west_wing_number_of_x_Pixels"
        )
        self.west_wing_number_of_y_Pixels = self.read_typed_value(
            root["Header"], "west_wing_number_of_y_Pixels"
        )
        self.west_wing_tank_center_internal_offset_mm = self.read_typed_value(
            root["Header"], "west_wing_tank_center_internal_offset_mm"
        )
        self.west_wing_det_radius_m = self.read_typed_value(
            root["Header"], "west_wing_det_radius_m"
        )
        self.west_wing_rot_offset_deg = self.read_typed_value(
            root["Header"], "west_wing_rot_offset_deg"
        )
        self.det_axis_offset_mm = self.read_typed_value(
            root["Header"], "det_axis_offset_mm"
        )
        self.x_mm_per_pixel = self.read_typed_value(root["Header"], "x_mm_per_pixel")
        self.y_mm_per_pixel = self.read_typed_value(root["Header"], "y_mm_per_pixel")
        self.absolute_intensity_constant = self.read_typed_value(
            root["Header"], "absolute_intensity_constant"
        )
        self.source_aperture_size = self.read_typed_value(
            root["Header"], "source_aperture_size"
        )
        self.sample_aperture_name = self.read_value(
            root["Header"], "sample_aperture_name"
        )
        self.sample_aperture_description = self.read_value(
            root["Header"], "sample_aperture_description"
        )
        self.sample_aperture_size = self.read_typed_value(
            root["Header"], "sample_aperture_size"
        )
        self.beamtrap_name = self.read_value(root["Header"], "beamtrap_name")
        self.beamtrap_diameter = self.read_typed_value(
            root["Header"], "beamtrap_diameter"
        )
        self.beamtrap_is_blocking = self.read_value(
            root["Header"], "beamtrap_is_blocking"
        )
        self.source_distance = self.read_typed_value(root["Header"], "source_distance")
        self.sample_to_flange = self.read_typed_value(
            root["Header"], "sample_to_flange"
        )
        self.sample_aperture_to_flange = self.read_typed_value(
            root["Header"], "sample_aperture_to_flange"
        )
        self.tank_internal_offset = self.read_typed_value(
            root["Header"], "tank_internal_offset"
        )
        self.wavelength_formula = self.read_value(root["Header"], "wavelength_formula")
        self.wavelength = self.read_typed_value(root["Header"], "wavelength")
        self.wavelength_spread = self.read_typed_value(
            root["Header"], "wavelength_spread"
        )
        self.source_distance = self.read_typed_value(root["Header"], "source_distance")
        self.Ref_Scan_Main_Flood = self.read_value(
            root["Header"], "Ref_Scan_Main_Flood"
        )
        self.Ref_Scan_Main_Beam_Center = self.read_value(
            root["Header"], "Ref_Scan_Main_Beam_Center"
        )
        self.Ref_Scan_Main_Dark_Current = self.read_value(
            root["Header"], "Ref_Scan_Main_Dark_Current"
        )
        self.Ref_Scan_Main_Bar = self.read_value(root["Header"], "Ref_Scan_Main_Bar")
        self.Ref_Scan_West_Wing_Flood = self.read_value(
            root["Header"], "Ref_Scan_West_Wing_Flood"
        )
        self.Ref_Scan_West_Wing_Dark_Current = self.read_value(
            root["Header"], "Ref_Scan_West_Wing_Dark_Current"
        )
        self.Ref_Scan_West_Wing_Bar = self.read_value(
            root["Header"], "Ref_Scan_West_Wing_Bar"
        )
        self.sans_spice_xml_format_version = self.read_typed_value(
            root["Header"], "sans_spice_xml_format_version"
        )
        self.Comment = self.read_value(root["Header"], "Comment")
        self.ImagePath = self.read_value(root["Header"], "ImagePath")
        # Sample Info
        self.Field = {}
        for key in root["sample_info"].keys():
            if root["sample_info"].get(key) is not None:
                for item in root["sample_info"][key].keys():
                    if key == "background" and item == "Field":
                        self.Field[
                            self.read_value(
                                root["sample_info"]["background"]["Field"], "@full_name"
                            )
                        ] = self.read_value(
                            root["sample_info"]["background"]["Field"], "#text"
                        )
        # Motor Positions
        self.highvoltagecmd = {}
        if root["Motor_Positions"]["highvoltagecmd"].keys() is not None:
            self.read_positions(
                root["Motor_Positions"]["highvoltagecmd"], self.highvoltagecmd
            )
        self.selector_speed = {}
        if root["Motor_Positions"]["selector_speed"].keys() is not None:
            self.read_positions(
                root["Motor_Positions"]["selector_speed"], self.selector_speed
            )
        self.selector_tilt = {}
        if root["Motor_Positions"]["selector_tilt"].keys() is not None:
            self.read_positions(
                root["Motor_Positions"]["selector_tilt"], self.selector_tilt
            )
        self._lambda = {}
        if root["Motor_Positions"]["lambda"].keys() is not None:
            self.read_positions(root["Motor_Positions"]["lambda"], self._lambda)
        self.dlambda = {}
        if root["Motor_Positions"]["dlambda"].keys() is not None:
            self.read_positions(root["Motor_Positions"]["dlambda"], self.dlambda)
        self.sdd = {}
        if root["Motor_Positions"]["sdd"].keys() is not None:
            self.read_positions(root["Motor_Positions"]["sdd"], self.sdd)
        self.coll_1 = {}
        if root["Motor_Positions"]["coll_1"].keys() is not None:
            self.read_positions(root["Motor_Positions"]["coll_1"], self.coll_1)
        self.coll_2 = {}
        if root["Motor_Positions"]["coll_2"].keys() is not None:
            self.read_positions(root["Motor_Positions"]["coll_2"], self.coll_2)
        self.coll_3 = {}
        if root["Motor_Positions"]["coll_3"].keys() is not None:
            self.read_positions(root["Motor_Positions"]["coll_3"], self.coll_3)
        self.coll_4 = {}
        if root["Motor_Positions"]["coll_4"].keys() is not None:
            self.read_positions(root["Motor_Positions"]["coll_4"], self.coll_4)
        self.coll_5 = {}
        if root["Motor_Positions"]["coll_5"].keys() is not None:
            self.read_positions(root["Motor_Positions"]["coll_5"], self.coll_5)
        self.coll_6 = {}
        if root["Motor_Positions"]["coll_6"].keys() is not None:
            self.read_positions(root["Motor_Positions"]["coll_6"], self.coll_6)
        self.coll_7 = {}
        if root["Motor_Positions"]["coll_7"].keys() is not None:
            self.read_positions(root["Motor_Positions"]["coll_7"], self.coll_7)
        self.coll_8 = {}
        if root["Motor_Positions"]["coll_8"].keys() is not None:
            self.read_positions(root["Motor_Positions"]["coll_8"], self.coll_8)
        self.nguides = {}
        if root["Motor_Positions"]["nguides"].keys() is not None:
            self.read_positions(root["Motor_Positions"]["nguides"], self.nguides)
        self.attenuator_pos = {}
        if root["Motor_Positions"]["attenuator_pos"].keys() is not None:
            self.read_positions(
                root["Motor_Positions"]["attenuator_pos"], self.attenuator_pos
            )
        self.beam_trap_x = {}
        if root["Motor_Positions"]["beam_trap_x"].keys() is not None:
            self.read_positions(
                root["Motor_Positions"]["beam_trap_x"], self.beam_trap_x
            )
        self.dcal = {}
        if root["Motor_Positions"]["dcal"].keys() is not None:
            self.read_positions(root["Motor_Positions"]["dcal"], self.dcal)
        self.detector_trans = {}
        if root["Motor_Positions"]["detector_trans"].keys() is not None:
            self.read_positions(
                root["Motor_Positions"]["detector_trans"], self.detector_trans
            )
        self.flange_det_dist = {}
        if root["Motor_Positions"]["flange_det_dist"].keys() is not None:
            self.read_positions(
                root["Motor_Positions"]["flange_det_dist"], self.flange_det_dist
            )
        self.sample_x = {}
        if root["Motor_Positions"]["sample_x"].keys() is not None:
            self.read_positions(root["Motor_Positions"]["sample_x"], self.sample_x)
        self.trap_y_101mm = {}
        if root["Motor_Positions"]["trap_y_101mm"].keys() is not None:
            self.read_positions(
                root["Motor_Positions"]["trap_y_101mm"], self.trap_y_101mm
            )
        self.trap_y_25mm = {}
        if root["Motor_Positions"]["trap_y_25mm"].keys() is not None:
            self.read_positions(
                root["Motor_Positions"]["trap_y_25mm"], self.trap_y_101mm
            )
        self.trap_y_50mm = {}
        if root["Motor_Positions"]["trap_y_50mm"].keys() is not None:
            self.read_positions(
                root["Motor_Positions"]["trap_y_50mm"], self.trap_y_50mm
            )
        self.trap_y_76mm = {}
        if root["Motor_Positions"]["trap_y_76mm"].keys() is not None:
            self.read_positions(
                root["Motor_Positions"]["trap_y_76mm"], self.trap_y_76mm
            )
        # Parameter Positions
        self.hvsts1 = {}
        if root["Parameter_Positions"]["hvsts1"].keys() is not None:
            self.read_positions(root["Parameter_Positions"]["hvsts1"], self.hvsts1)
        self.hvsts2 = {}
        if root["Parameter_Positions"]["hvsts2"].keys() is not None:
            self.read_positions(root["Parameter_Positions"]["hvsts2"], self.hvsts2)
        self.hvsts3 = {}
        if root["Parameter_Positions"]["hvsts3"].keys() is not None:
            self.read_positions(root["Parameter_Positions"]["hvsts3"], self.hvsts3)
        self.vs_current = {}
        if root["Parameter_Positions"]["vs_current"].keys() is not None:
            self.read_positions(
                root["Parameter_Positions"]["vs_current"], self.vs_current
            )
        self.vs_speed_pv = {}
        if root["Parameter_Positions"]["vs_speed_pv"].keys() is not None:
            self.read_positions(
                root["Parameter_Positions"]["vs_speed_pv"], self.vs_speed_pv
            )
        self.beam_on = {}
        if root["Parameter_Positions"]["beam_on"].keys() is not None:
            self.read_positions(root["Parameter_Positions"]["beam_on"], self.beam_on)
        # Counters
        self.time = {}
        if root["Counters"]["time"].keys() is not None:
            self.read_counters(root["Counters"]["time"], self.time)
        self.detector = {}
        if root["Counters"]["detector"].keys() is not None:
            self.read_counters(root["Counters"]["detector"], self.detector)
        self.monitor = {}
        if root["Counters"]["monitor"].keys() is not None:
            self.read_counters(root["Counters"]["monitor"], self.monitor)
        # Data
        self.data_description = self.read_value(root["Data"], "@description")
        temp = self.read_value(root["Data"]["Detector"], "@type")
        if temp[0:3] == "INT":
            data = np.fromstring(
                self.read_value(root["Data"]["Detector"], "#text"),
                dtype=np.intc,
                sep=" ",
            )
        else:
            data = np.fromstring(
                self.read_value(root["Data"]["Detector"], "#text"),
                dtype=np.single,
                sep=" ",
            )
        det = data.reshape(self.Number_of_X_Pixels, self.Number_of_Y_Pixels)
        self.det1_data = det.transpose()
        self.nx1, self.ny1 = self.det1_data.shape
        return

    def read_value(self, root, item, default=None):
        value = root.get(item)
        if value is None:
            # print(item, default)
            return default
        else:
            # print(item, value)
            return value

    def read_typed_value(self, root, item, default=None):
        value = root.get(item)
        if value is None:
            # print(item, default)
            return default
        else:
            typed = self.read_value(root[item], "@type")
            if typed == "FLOAT32":
                value = float(self.read_value(root[item], "#text"))
                # print(item, "FLOAT32", value)
                return value
            elif typed == "INT32":
                value = int(self.read_value(root[item], "#text"))
                # print(item, "INT32", value)
                return value
            else:
                # print(item, default)
                return default

    def read_positions(self, root, dict):
        dict["pos"] = self.read_value(root, "@pos")
        dict["units"] = self.read_value(root, "@units")
        dict["description"] = self.read_value(root, "@description")
        dict["type"] = self.read_value(root, "@type")
        dict["value"] = self.read_value(root, "#text")
        # print(dict)

    def read_counters(self, root, dict):
        dict["units"] = self.read_value(root, "@units")
        dict["description"] = self.read_value(root, "@description")
        dict["type"] = self.read_value(root, "@type")
        dict["value"] = self.read_value(root, "#text")
        # print(dict)
