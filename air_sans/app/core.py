import os
import numpy
import logging

from trame.app import get_server
from trame.decorators import TrameApp, change
from trame.ui.vuetify import SinglePageWithDrawerLayout
from trame.widgets import vuetify, plotly

from .ui import (
    DeviceSelector,
    Directory,
    FileSelector,
    FigureControl,
    Scattering,
    Transmission,
)
from .instrument.d11_plus import D11_Plus
from .visualization import Visualization
from .utilities import file_search as fs
from .utilities import file_load as fl

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

PANELS = [
    ("device", "mdi-microscope"),
    ("directory", "mdi-folder-eye"),
    ("file", "mdi-application"),
    ("viz", "mdi-image-multiple"),
    ("scattering", "mdi-scatter-plot"),
    ("transmission", "mdi-transfer"),
]


# ---------------------------------------------------------
# Engine class
# ---------------------------------------------------------


@TrameApp()
class AirSans:
    def __init__(self, server=None, data=None):
        self.server = get_server(server, client_type="vue2")
        self._viz = Visualization(self.server)
        self._selected_device = None
        self._active_directory = None

        # CLI
        self.server.cli.add_argument(
            "--data",
            help="Path to browse",
            dest="data",
            default=".",
        )
        args, _ = self.server.cli.parse_known_args()
        if data is None:
            data = args.data

        # search directory contents
        self.state.dirs = fs.get_directory_structure(data)
        self.state.files = []
        self.state.file = None

        # Initialize data
        self.state.data = None
        self.state.center_data = None
        self.state.pixel_ratio = 2.0

        self.ui = self._build_ui()

    @property
    def state(self):
        return self.server.state

    @property
    def ctrl(self):
        return self.server.controller

    def _build_ui(self):
        self.state.trame__title = "air-sans"
        with SinglePageWithDrawerLayout(self.server) as layout:
            with layout.icon:
                vuetify.VIcon("mdi-bullseye")

            with layout.title as title:
                title.set_text("AIR-SANS")
                title.classes = "font-weight-medium ml-0 pl-0"

            with layout.toolbar as tb:
                tb.dense = True
                with vuetify.VBtnToggle(
                    v_model=("panel_visible", ["device", "directory", "file", "viz"]),
                    multiple=True,
                    dense=True,
                    classes="ml-6",
                ):
                    for key, icon in PANELS:
                        with vuetify.VBtn(value=key, small=True):
                            vuetify.VIcon(icon, small=True)

                vuetify.VSpacer()

            with layout.drawer as drawer:
                drawer.width = 350

                DeviceSelector()
                Directory(select_directory_fn=self.select_directory)
                FileSelector(self.selected_file)
                FigureControl()
                Scattering()
                Transmission()

            with layout.content:
                with vuetify.VContainer(
                    fluid=True,
                    classes="pa-0 fill-height",
                ):
                    self.ctrl.update_d11 = plotly.Figure(
                        display_mode_bar=("false",),
                        v_show=("figure_ready", False),
                    ).update

            return layout

    @change("selectedDevice")
    def on_device_change(self, selectedDevice, **kwargs):
        if selectedDevice == "D11+":
            self._selected_device = D11_Plus()

    def select_directory(self, active_nodes):
        self.server.state.directory_label = None
        self._active_directory = None
        if len(active_nodes):
            node_id = active_nodes[0]
            if isinstance(node_id, str):
                self.server.state.directory_label = os.path.basename(node_id)
                self._active_directory = node_id
                self.server.state.files = fs.get_file_list(node_id)

    def selected_file(self, file):
        state = self.server.state
        state.file = file
        data = fl.load(self._active_directory, state.file)
        pixel_y = 1.0
        pixel_x = 1.0
        # print(pixel_y / pixel_x, pixel_x, type(pixel_x), pixel_y, type(pixel_y))
        pixel_y = data["/entry0/D11/Detector 1/pixel_size_y"].nxdata[0].item()
        pixel_x = data["/entry0/D11/Detector 1/pixel_size_x"].nxdata[0].item()
        # print(pixel_y / pixel_x, pixel_x, type(pixel_x), pixel_y, type(pixel_y))
        state.pixel_ratio = pixel_y / pixel_x
        # print(state.pixel_ratio)

        detector1 = data["/entry0/D11/Detector 1/data"]
        detector1_2d = detector1[:, :, 0]
        ny, nx = detector1_2d.shape
        state.center_ny = ny
        state.center_nx = nx
        d1 = numpy.zeros(detector1_2d.shape, dtype=numpy.int32, order="C")
        for i in range(0, nx - 1):
            for j in range(0, ny - 1):
                d1[j, i] = detector1_2d[j, i]
        self._viz.set_center_data(d1.transpose())

        detector2 = data["/entry0/D11/Detector 2/data"]
        detector2_2d = detector2[:, :, 0]
        ny, nx = detector2_2d.shape
        state.left_ny = ny
        state.left_nx = nx
        d2 = numpy.zeros(detector2_2d.shape, dtype=numpy.int32, order="C")
        for i in range(0, nx - 1):
            for j in range(0, ny - 1):
                d2[j, i] = detector2_2d[j, i]
        self._viz.set_left_data(d2.transpose())

        detector3 = data["/entry0/D11/Detector 3/data"]
        detector3_2d = detector3[:, :, 0]
        ny, nx = detector3_2d.shape
        state.right_ny = ny
        state.right_nx = nx
        d3 = numpy.zeros(detector3_2d.shape, dtype=numpy.int32, order="C")
        for i in range(0, nx - 1):
            for j in range(0, ny - 1):
                d3[j, i] = detector3_2d[j, i]
        self._viz.set_right_data(d3.transpose())

        self._viz.create_d11_fig()
        state.figure_ready = True

    @change("device_active_data")
    def show_imask(self, device_active_data, **kwargs):
        self.server.state.figure_ready = False

        if device_active_data == "mask":
            self._viz.set_center_data(self._selected_device.detector1_imask_data)
            self._viz.set_left_data(self._selected_device.detector2_imask_data)
            self._viz.set_right_data(self._selected_device.detector3_imask_data)
            self.server.state.figure_ready = True
            self._viz.create_d11_fig()

        if device_active_data == "efficiency":
            self._viz.set_center_data(self._selected_device.detector1_efficiency_data)
            self._viz.set_left_data(self._selected_device.detector2_efficiency_data)
            self._viz.set_right_data(self._selected_device.detector3_efficiency_data)
            self.server.state.figure_ready = True
            self._viz.create_d11_fig()

        if device_active_data == "error":
            self._viz.set_center_data(self._selected_device.detector1_efficiency_error)
            self._viz.set_left_data(self._selected_device.detector2_efficiency_error)
            self._viz.set_right_data(self._selected_device.detector3_efficiency_error)
            self.server.state.figure_ready = True
            self._viz.create_d11_fig()

        if device_active_data == "" and self.server.state.file:
            self.selected_file(self.server.state.file)
