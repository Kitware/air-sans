# import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from trame.decorators import TrameApp, change

from .vtk import DetectorView


@TrameApp()
class Visualization:
    def __init__(self, server):
        self.server = server
        self._left_data = None
        self._center_data = None
        self._right_data = None
        self._left_view = DetectorView(server, False)
        self._center_view = DetectorView(server, True)
        self._right_view = DetectorView(server, False)

    def set_left_data(self, data, x, y):
        self._left_data = data
        self._left_view.update_data(data, x, y)

    def set_center_data(self, data, x, y):
        # data = np.fromfile("/Users/sebastien.jourdain/Downloads/heatmap_gpsans.np").reshape(500, 49152)
        self._center_data = data
        self._center_view.update_data(data, x, y)
        # self._center_view.update_data(data, 1, 100)

    def set_right_data(self, data, x, y):
        self._right_data = data
        self._right_view.update_data(data, x, y)

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

    @change(
        "selectedRepresentation",
        "contour_labels",
        "selectedColor",
        "center_nx",
        "center_ny",
        "pixel_ratio",
        "left_nx",
        "left_ny",
        "right_nx",
        "right_ny",
    )
    def create_d11_fig(self, **kwargs):
        state = self.server.state

        print("pixel_ratio", state.pixel_ratio)

        fig = make_subplots(
            rows=5,
            cols=4,
            specs=[
                [None, {"rowspan": 5, "colspan": 2}, None, None],
                [
                    {"rowspan": 3, "colspan": 1},
                    None,
                    None,
                    {"rowspan": 3, "colspan": 1},
                ],
                [None, None, None, None],
                [None, None, None, None],
                [None, None, None, None],
            ],
            print_grid=False,
        )
        # center (1,2), left (2,1), right (2,4)
        if state.selectedRepresentation == "Heatmap":
            self.create_heatmap(fig, self._center_data, 1, 2)
        elif state.selectedRepresentation == "Contours":
            self.create_contour(fig, self._center_data, 1, 2)
        else:
            self.create_combined(fig, self._center_data, 1, 2)
        fig.update_yaxes(
            range=(0.0, state.center_nx),
            constrain="domain",
            scaleanchor="x",
            scaleratio=state.pixel_ratio,
            row=1,
            col=2,
        )
        fig.update_xaxes(
            range=(0.0, state.center_ny), constrain="domain", scaleratio=2, row=1, col=2
        )
        if state.selectedRepresentation == "Heatmap":
            self.create_heatmap(fig, self._left_data, 2, 1)
        elif state.selectedRepresentation == "Contours":
            self.create_contour(fig, self._left_data, 2, 1)
        else:
            self.create_combined(fig, self._left_data, 2, 1)
        fig.update_yaxes(range=(0.0, state.left_nx), constrain="domain", row=2, col=1)
        fig.update_xaxes(
            range=(0.0, state.left_ny),
            constrain="domain",
            scaleanchor="y",
            scaleratio=1,
            row=2,
            col=1,
        )
        if state.selectedRepresentation == "Heatmap":
            self.create_heatmap(fig, self._right_data, 2, 4)
        elif state.selectedRepresentation == "Contours":
            self.create_contour(fig, self._right_data, 2, 4)
        else:
            self.create_combined(fig, self._right_data, 2, 4)
        fig.update_yaxes(range=(0.0, state.right_nx), constrain="domain", row=2, col=4)
        fig.update_xaxes(
            range=(0.0, state.right_ny),
            constrain="domain",
            scaleanchor="y",
            scaleratio=1,
            row=2,
            col=4,
        )
        fig.update_layout(
            coloraxis=dict(colorscale=state.selectedColor), showlegend=False
        )

        print("FIXME no more plotly....")
        # self.server.controller.update_d11(fig)

        return fig

    def create_heatmap(self, fig, data, _row, _col, **kwargs):
        fig.add_trace(
            go.Heatmap(
                z=data,
                coloraxis="coloraxis",
            ),
            row=_row,
            col=_col,
        )

    def create_contour(self, fig, data, _row, _col, **kwargs):
        state = self.server.state

        fig.add_trace(
            go.Contour(
                z=data,
                contours={
                    "coloring": "lines",
                    "showlabels": state.contour_labels,
                    "labelfont": {
                        "size": 12,
                        "color": "black",
                    },
                },
                contours_coloring="lines",
                line_smoothing=1,
                coloraxis="coloraxis",
                name="(1,2)",
            ),
            row=_row,
            col=_col,
        )

    def create_combined(self, fig, data, _row, _col, **kwargs):
        state = self.server.state

        fig.add_trace(
            go.Contour(
                z=data,
                contours={
                    "coloring": "heatmap",
                    "showlabels": state.contour_labels,
                    "labelfont": {
                        "size": 12,
                        "color": "black",
                    },
                },
                line_smoothing=1,
                coloraxis="coloraxis",
                name="(1,2)",
            ),
            row=_row,
            col=_col,
        )
