import os
import logging

from trame.app import get_server
from trame.decorators import TrameApp, change
from trame.ui.vuetify import SinglePageWithDrawerLayout
from trame.widgets import vuetify, plotly, vtk

from .assets import ASSETS
from .ui import (
    DeviceSelector,
    Directory,
    FileSelector,
    FigureControl,
    Scattering,
    Transmission,
)
from .instrument.d11_plus import D11_Plus
from .instrument.cg2 import CG2
from .visualization import Visualization
from .utilities import file_search as fs

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
# AirSans class
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

        # Detectors
        self.state.left_detector = False
        self.state.center_detector = False
        self.state.right_detector = False

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
                with vuetify.VBtnToggle(
                    dense=True,
                    classes="ml-6",
                    v_model=("renderer", "plotly"),
                    hide_details=True,
                    mandatory=True,
                ):
                    with vuetify.VBtn(
                        small=True,
                        icon=True,
                        value="plotly",
                    ):
                        vuetify.VImg(
                            src=ASSETS.plotly, height=20, width=20, contain=True
                        )
                    with vuetify.VBtn(
                        small=True,
                        icon=True,
                        value="vtk",
                    ):
                        vuetify.VImg(src=ASSETS.vtk, height=20, width=20, contain=True)

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
                    with vuetify.VRow(
                        v_show="selectedDevice == 'CG2' && renderer == 'vtk'",
                        classes="fill-height pa-0",
                    ):
                        with vuetify.VCol(
                            cols=12, v_show="center_detector", classes="pa-0"
                        ):
                            view = vtk.VtkRemoteView(
                                self._viz.full_render_window, interactive_ratio=1
                            )
                            self._viz.set_full_view(view)
                    with vuetify.VRow(
                        v_show="selectedDevice == 'D11+' && renderer == 'vtk'",
                        classes="fill-height pa-0",
                    ):
                        with vuetify.VCol(
                            cols=3, v_show="left_detector", classes="pa-0"
                        ):
                            view = vtk.VtkRemoteView(
                                self._viz.left_render_window, interactive_ratio=1
                            )
                            self._viz.set_left_view(view)
                        with vuetify.VCol(
                            cols=6, v_show="center_detector", classes="pa-0"
                        ):
                            view = vtk.VtkRemoteView(
                                self._viz.center_render_window, interactive_ratio=1
                            )
                            self._viz.set_center_view(view)
                        with vuetify.VCol(
                            cols=3,
                            v_show="right_detector",
                            classes="pa-0",
                        ):
                            view = vtk.VtkRemoteView(
                                self._viz.right_render_window, interactive_ratio=1
                            )
                            self._viz.set_right_view(view)
                    with vuetify.VRow(
                        v_show="renderer == 'plotly'", classes="fill-height pa-0"
                    ):
                        self.ctrl.plotly_view_update = plotly.Figure(
                            display_mode_bar=("false",),
                            v_show=("figure_ready", False),
                        ).update

            return layout

    @change("selectedDevice")
    def on_device_change(self, selectedDevice, **kwargs):
        if selectedDevice == "D11+":
            self._viz.set_selected_device("D11+")
            self._selected_device = D11_Plus()
            self.state.left_detector = True
            self.state.center_detector = True
            self.state.right_detector = True
            self._viz.set_center_mask(self._selected_device.detector1_mask)
            self._viz.set_left_mask(self._selected_device.detector2_mask)
            self._viz.set_right_mask(self._selected_device.detector3_mask)
        elif selectedDevice == "CG2":
            self._viz.set_selected_device("CG2")
            self._selected_device = CG2()
            self.state.left_detector = True
            self.state.center_detector = True
            self.state.right_detector = True
            self._viz.set_center_mask(self._selected_device.detector1_mask)

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
        if self._selected_device.Instrument == "D11+":
            self.open_d11plus_file(file)
        elif self._selected_device.Instrument == "CG2":
            self.open_cg2_file(file)
        else:
            return

    def open_cg2_file(self, file):
        state = self.server.state
        state.file = file
        self._selected_device.read_file(self._active_directory, state.file)
        self._viz.reset_data_minmax()
        pixel1_x = self._selected_device.detector1_pixel_size[0]
        pixel1_y = self._selected_device.detector1_pixel_size[1]
        state.pixel_ratio = pixel1_y / pixel1_x
        state.center_ny = self._selected_device.ny1
        state.center_nx = self._selected_device.nx1
        self._viz.set_center_data(self._selected_device.det1_data, pixel1_x, pixel1_y)

        self._viz.update_visualization()

        state.figure_ready = True

    def open_d11plus_file(self, file):
        state = self.server.state
        state.file = file
        self._selected_device.read_file(self._active_directory, state.file)
        self._viz.reset_data_minmax()

        pixel1_x = self._selected_device.pixel1_x
        pixel1_y = self._selected_device.pixel1_y
        state.pixel_ratio = pixel1_y / pixel1_x
        state.center_ny = self._selected_device.ny1
        state.center_nx = self._selected_device.nx1
        self._viz.set_center_data(self._selected_device.det1_data, pixel1_x, pixel1_y)

        pixel2_x = self._selected_device.pixel2_x
        pixel2_y = self._selected_device.pixel2_y
        state.left_ny = self._selected_device.ny2
        state.left_nx = self._selected_device.nx2
        self._viz.set_left_data(self._selected_device.det2_data, pixel2_x, pixel2_y)

        pixel3_x = self._selected_device.pixel3_x
        pixel3_y = self._selected_device.pixel3_y
        state.right_ny = self._selected_device.ny3
        state.right_nx = self._selected_device.nx3
        self._viz.set_right_data(self._selected_device.det3_data, pixel3_x, pixel3_y)

        self._viz.update_visualization()

        state.figure_ready = True

    @change("device_active_data")
    def show_imask(self, device_active_data, **kwargs):
        self.server.state.figure_ready = False
        if device_active_data == "mask":
            pixel1_x = self._selected_device.pixel1_x
            pixel1_y = self._selected_device.pixel1_y
            pixel2_x = self._selected_device.pixel2_x
            pixel2_y = self._selected_device.pixel2_y
            pixel3_x = self._selected_device.pixel3_x
            pixel3_y = self._selected_device.pixel3_y
            self._viz.set_center_data(
                self._selected_device.detector1_imask_data, pixel1_x, pixel1_y
            )
            self._viz.set_left_data(
                self._selected_device.detector2_imask_data, pixel2_x, pixel2_y
            )
            self._viz.set_right_data(
                self._selected_device.detector3_imask_data, pixel3_x, pixel3_y
            )
            self.server.state.figure_ready = True
            self._viz.update_visualization()

        if device_active_data == "efficiency":
            pixel1_x = self._selected_device.pixel1_x
            pixel1_y = self._selected_device.pixel1_y
            pixel2_x = self._selected_device.pixel2_x
            pixel2_y = self._selected_device.pixel2_y
            pixel3_x = self._selected_device.pixel3_x
            pixel3_y = self._selected_device.pixel3_y
            self._viz.set_center_data(
                self._selected_device.detector1_efficiency_data, pixel1_x, pixel1_y
            )
            self._viz.set_left_data(
                self._selected_device.detector2_efficiency_data, pixel2_x, pixel2_y
            )
            self._viz.set_right_data(
                self._selected_device.detector3_efficiency_data, pixel3_x, pixel3_y
            )
            self.server.state.figure_ready = True
            self._viz.update_visualization()

        if device_active_data == "error":
            pixel1_x = self._selected_device.pixel1_x
            pixel1_y = self._selected_device.pixel1_y
            pixel2_x = self._selected_device.pixel2_x
            pixel2_y = self._selected_device.pixel2_y
            pixel3_x = self._selected_device.pixel3_x
            pixel3_y = self._selected_device.pixel3_y
            self._viz.set_center_data(
                self._selected_device.detector1_efficiency_error, pixel1_x, pixel1_y
            )
            self._viz.set_left_data(
                self._selected_device.detector2_efficiency_error, pixel2_x, pixel2_y
            )
            self._viz.set_right_data(
                self._selected_device.detector3_efficiency_error, pixel3_x, pixel3_y
            )
            self.server.state.figure_ready = True
            self._viz.update_visualization()

        if device_active_data == "" and self.server.state.file:
            self.selected_file(self.server.state.file)
