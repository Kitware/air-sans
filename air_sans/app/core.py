r"""
Define your classes and create the instances that you need to expose
"""
import os

import numpy

import logging
from trame.app import get_server

from .visualization import create_visualization

from .utilities import file_search as fs
from .utilities import file_load as fl

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# ---------------------------------------------------------
# Engine class
# ---------------------------------------------------------
search_directory = "/Users/patrick.oleary/Desktop/share"


class Engine:
    def __init__(self, server):
        self._server = server

        # initialize state + controller
        state, ctrl = server.state, server.controller

        Visualization = create_visualization(server)
        self.Visualization = Visualization

        # search directory contents
        dirs = fs.get_directory_structure(search_directory)
        state.devices = ["D11", "D11+"]
        state.selectedDevice = None
        state.directory = None
        state.directory_label = None
        state.dirs = dirs
        state.dirtree = []
        state.directory_dialog = False
        state.files = []
        state.file_selected = None
        state.file = None

        # Initialize data
        state.data = None
        state.center_data = None
        state.scattering_samples_28m = []
        state.scattering_samples_8m = []
        state.scattering_samples_2m = []
        state.scattering_empty_cell_28m = []
        state.scattering_empty_cell_8m = []
        state.scattering_empty_cell_2m = []
        state.scattering_blocked_beam_28m = []
        state.scattering_blocked_beam_8m = []
        state.scattering_blocked_beam_2m = []
        state.transmission_samples_28m = []
        state.transmission_samples_8m = []
        state.transmission_samples_2m = []
        state.transmission_empty_cell_28m = []
        state.transmission_empty_cell_8m = []
        state.transmission_empty_cell_2m = []
        state.transmission_direct_beam_28m = []
        state.transmission_direct_beam_8m = []
        state.transmission_direct_beam_2m = []

        # Set workflows state
        state.directory_workflow = False
        state.browse_workflow = False
        state.scattering_workflow = False
        state.transmission_workflow = False
        state.image_workflow = False

        # Set state visualization
        state.pixel_ratio = 1.0
        state.representations = ["Heatmap", "Contours", "Combined"]
        state.selectedRepresentation = "Heatmap"
        state.colors = ["spectral", "rdbu", "gray", "blackbody", "sunset"]
        state.selectedColor = "spectral"
        state.contour_labels = True

        # Set state variable
        state.trame__title = "air-sans"
        state.resolution = 6

        # Bind instance methods to controller
        ctrl.reset_resolution = self.reset_resolution
        ctrl.widget_click = self.widget_click
        ctrl.widget_change = self.widget_change
        ctrl.trigger_directory_dialog = self.trigger_directory_dialog
        ctrl.trigger_directory_selection = self.trigger_directory_selection
        ctrl.selected_file = self.selected_file

        # Bind instance methods to state change
        state.change("resolution")(self.on_resolution_change)

        @state.change("d11_size")
        def update_left_contour_size(d11_size, **kwargs):
            if d11_size is None:
                return

            ctrl.update_d11(Visualization.create_d11_fig(**d11_size.get("size")))

    # @state.change("left_contour_size")
    # def update_left_contour_size(left_contour_size, **kwargs):
    #   if left_contour_size is None:
    #       return
    #
    #   ctrl.update_left_contour(Visualization.create_left_contour_fig(**left_contour_size.get("size")))

    # @state.change("center_contour_size")
    # def update_center_contour_size(center_contour_size, **kwargs):
    #    if center_contour_size is None:
    #        return

    #    ctrl.update_center_contour(Visualization.create_center_contour_fig(**center_contour_size.get("size")))

    # @state.change("right_contour_size")
    # def update_right_contour_size(right_contour_size, **kwargs):
    #    if right_contour_size is None:
    #        return
    #
    #    ctrl.update_right_contour(Visualization.create_right_contour_fig(**right_contour_size.get("size")))

    @property
    def server(self):
        return self._server

    @property
    def state(self):
        return self.server.state

    @property
    def ctrl(self):
        return self.server.controller

    def show_in_jupyter(self, **kwargs):
        from trame.app import jupyter

        logger.setLevel(logging.WARNING)
        jupyter.show(self.server, **kwargs)

    def reset_resolution(self):
        self._server.state.resolution = 6

    def on_resolution_change(self, resolution, **kwargs):
        logger.info(f">>> ENGINE(a): Slider updating resolution to {resolution}")

    def widget_click(self):
        logger.info(">>> ENGINE(a): Widget Click")

    def widget_change(self):
        logger.info(">>> ENGINE(a): Widget Change")

    def trigger_directory_dialog(self):
        self._server.state.directory_dialog = not self._server.state.directory_dialog

    def trigger_directory_selection(self, active_nodes):
        self._server.state.directory_label = None
        self._server.state.directory = None
        if len(active_nodes):
            node_id = active_nodes[0]
            if isinstance(node_id, str):
                self._server.state.directory_label = os.path.basename(node_id)
                self._server.state.directory = node_id
                self._server.state.files = fs.get_file_list(node_id)

    def selected_file(self, file):
        state = self._server.state
        ctrl = self._server.controller
        state.file = file
        data = fl.load(state.directory, state.file)
        pixel_y = 1.0
        pixel_x = 1.0
        print(pixel_y / pixel_x, pixel_x, type(pixel_x), pixel_y, type(pixel_y))
        pixel_y = data["/entry0/D11/Detector 1/pixel_size_y"].nxdata[0].item()
        pixel_x = data["/entry0/D11/Detector 1/pixel_size_x"].nxdata[0].item()
        print(pixel_y / pixel_x, pixel_x, type(pixel_x), pixel_y, type(pixel_y))
        state.pixel_ratio = pixel_y / pixel_x
        print(state.pixel_ratio)

        detector1 = data["/entry0/D11/Detector 1/data"]
        detector1_2d = detector1[:, :, 0]
        ny, nx = detector1_2d.shape
        state.center_ny = ny
        state.center_nx = nx
        d1 = numpy.zeros(detector1_2d.shape, dtype=numpy.int32, order="C")
        for i in range(0, nx - 1):
            for j in range(0, ny - 1):
                d1[j, i] = detector1_2d[j, i]
        self.Visualization.set_center_data(d1.transpose())

        detector2 = data["/entry0/D11/Detector 2/data"]
        detector2_2d = detector2[:, :, 0]
        ny, nx = detector2_2d.shape
        state.left_ny = ny
        state.left_nx = nx
        d2 = numpy.zeros(detector2_2d.shape, dtype=numpy.int32, order="C")
        for i in range(0, nx - 1):
            for j in range(0, ny - 1):
                d2[j, i] = detector2_2d[j, i]
        self.Visualization.set_left_data(d2.transpose())

        detector3 = data["/entry0/D11/Detector 3/data"]
        detector3_2d = detector3[:, :, 0]
        ny, nx = detector3_2d.shape
        state.right_ny = ny
        state.right_nx = nx
        d3 = numpy.zeros(detector3_2d.shape, dtype=numpy.int32, order="C")
        for i in range(0, nx - 1):
            for j in range(0, ny - 1):
                d3[j, i] = detector3_2d[j, i]
        self.Visualization.set_right_data(d3.transpose())

        # ctrl.update_left_contour(self.Visualization.create_left_contour_fig())
        # ctrl.update_center_contour(self.Visualization.create_center_contour_fig())
        # ctrl.update_right_contour(self.Visualization.create_right_contour_fig())
        ctrl.update_d11(self.Visualization.create_d11_fig())


def create_engine(server=None):
    # Get or create server
    if server is None:
        server = get_server(client_type="vue2")

    if isinstance(server, str):
        server = get_server(server, client_type="vue2")

    return Engine(server)
