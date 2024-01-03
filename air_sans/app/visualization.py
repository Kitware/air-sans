import numpy as np

from trame.decorators import TrameApp, change

from .vtk import VTKDetectorView
from .plotly import PlotlyDetectorView


@TrameApp()
class Visualization:
    def __init__(self, server):
        self.server = server
        self.selected_device = None
        self._data_max = -2147483648
        self._data_min = 2147483648
        self._left_data = None
        self._left_mask = None
        self._left_x = None
        self._left_y = None
        self._center_data = None
        self._center_mask = None
        self._center_x = None
        self._center_y = None
        self._right_data = None
        self._right_mask = None
        self._right_x = None
        self._right_y = None
        # VTK Views
        self._full_view = VTKDetectorView(server, True)
        self._left_view = VTKDetectorView(server, False)
        self._center_view = VTKDetectorView(server, True)
        self._right_view = VTKDetectorView(server, False)
        # Plotly Views
        self._all_view = PlotlyDetectorView(server)

    def set_selected_device(self, device):
        self.selected_device = device

    def reset_data_minmax(self):
        self._data_max = -2147483648
        self._data_min = 2147483648

    def set_left_data(self, data, x, y):
        self._left_data = data
        tmp_min = np.min(data)
        tmp_max = np.max(data)
        self._data_min = min(self._data_min, tmp_min)
        self._data_max = max(self._data_max, tmp_max)
        self._left_x = x
        self._left_y = y

    def set_center_data(self, data, x, y):
        self._center_data = data
        tmp_min = np.min(data)
        tmp_max = np.max(data)
        self._data_min = min(self._data_min, tmp_min)
        self._data_max = max(self._data_max, tmp_max)
        self._center_x = x
        self._center_y = y

    def set_right_data(self, data, x, y):
        self._right_data = data
        tmp_min = np.min(data)
        tmp_max = np.max(data)
        self._data_min = min(self._data_min, tmp_min)
        self._data_max = max(self._data_max, tmp_max)
        self._right_x = x
        self._right_y = y

    def set_left_mask(self, mask):
        self._left_mask = mask

    def set_center_mask(self, mask):
        self._center_mask = mask

    def set_right_mask(self, mask):
        self._right_mask = mask

    @change(
        "renderer",
        "selectedRepresentation",
        "contour_labels",
        "show_mask",
        "selectedColor",
        "center_nx",
        "center_ny",
        "pixel_ratio",
        "left_nx",
        "left_ny",
        "right_nx",
        "right_ny",
    )
    def update_visualization(self, **kwargs):
        if self.selected_device == "D11+":
            self.update_d11_visualization()
        elif self.selected_device == "CG2":
            self.update_cg2_visualization()

    def update_d11_visualization(self, **kwargs):
        if self.server.state.renderer != "plotly":
            self.update_d11_vtk()
        else:
            self.update_d11_plotly()

    def update_cg2_visualization(self, **kwargs):
        if self.server.state.renderer != "plotly":
            self.update_cg2_vtk()
        else:
            self.update_cg2_plotly()

    ################################
    # VTK
    ################################

    @property
    def full_render_window(self):
        return self._full_view.render_window

    def set_full_view(self, html_view):
        self._full_view.set_html_view(html_view)

    @property
    def left_render_window(self):
        return self._left_view.render_window

    def set_left_view(self, html_view):
        self._left_view.set_html_view(html_view)

    @property
    def center_render_window(self):
        return self._center_view.render_window

    def set_center_view(self, html_view):
        self._center_view.set_html_view(html_view)

    @property
    def right_render_window(self):
        return self._right_view.render_window

    def set_right_view(self, html_view):
        self._right_view.set_html_view(html_view)

    def reset_camera(self):
        self._left_view.html_reset_camera()
        self._center_view.html_reset_camera()
        self._right_view.html_reset_camera()

    def update_d11_vtk(self, **kwargs):
        self._left_view.set_data_minmax(self._data_min, self._data_max)
        self._left_view.update_data(
            self._left_data, self._left_mask, self._left_x, self._left_y
        )
        self._center_view.set_data_minmax(self._data_min, self._data_max)
        self._center_view.update_data(
            self._center_data, self._center_mask, self._center_x, self._center_y
        )
        self._right_view.set_data_minmax(self._data_min, self._data_max)
        self._right_view.update_data(
            self._right_data, self._right_mask, self._right_x, self._right_y
        )

    def update_cg2_vtk(self, **kwargs):
        self._full_view.set_data_minmax(self._data_min, self._data_max)
        self._full_view.update_data(
            self._center_data, self._center_mask, self._center_x, self._center_y
        )

    ################################
    # Plotly
    ################################

    def update_d11_plotly(self, **kwargs):
        self._all_view.set_data_minmax(self._data_min, self._data_max)
        self._all_view.update_left_data(
            self._left_data, self._left_mask, self._left_x, self._left_y
        )
        self._all_view.update_center_data(
            self._center_data, self._center_mask, self._center_x, self._center_y
        )
        self._all_view.update_right_data(
            self._right_data, self._right_mask, self._right_x, self._right_y
        )
        self._all_view.update_d11_view()

    def update_cg2_plotly(self, **kwargs):
        self._all_view.set_data_minmax(self._data_min, self._data_max)
        self._all_view.update_center_data(
            self._center_data, self._center_mask, self._center_x, self._center_y
        )
        self._all_view.update_cg2_view()
