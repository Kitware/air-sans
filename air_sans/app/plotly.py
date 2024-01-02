from trame.decorators import TrameApp

import plotly.graph_objects as go
from plotly.subplots import make_subplots


@TrameApp()
class PlotlyDetectorView:
    def __init__(self, server):
        self.server = server

        self.color_range = [0, 1]
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

    def set_data_minmax(self, data_min, data_max):
        self.color_range = [data_min, data_max]

    def update_left_data(self, data, mask, x, y, **kwargs):
        self._left_data = data
        self._left_mask = mask
        self._left_x = x
        self._left_y = y

    def update_center_data(self, data, mask, x, y, **kwargs):
        self._center_data = data
        self._center_mask = mask
        self._center_x = x
        self._center_y = y

    def update_right_data(self, data, mask, x, y, **kwargs):
        self._right_data = data
        self._right_mask = mask
        self._right_x = x
        self._right_y = y

    def update_d11_view(self, **kwargs):
        state = self.server.state

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

        # center
        if state.selectedRepresentation == "Heatmap":
            self.create_heatmap(fig, self._center_data, self._center_mask, 1, 2)
        elif state.selectedRepresentation == "Contours":
            self.create_contour(fig, self._center_data, 1, 2)
        else:
            self.create_combined(fig, self._center_data, self._center_mask, 1, 2)
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

        # left
        if state.selectedRepresentation == "Heatmap":
            self.create_heatmap(fig, self._left_data, self._left_mask, 2, 1)
        elif state.selectedRepresentation == "Contours":
            self.create_contour(fig, self._left_data, 2, 1)
        else:
            self.create_combined(fig, self._left_data, self._left_mask, 2, 1)
        fig.update_yaxes(range=(0.0, state.left_nx), constrain="domain", row=2, col=1)
        fig.update_xaxes(
            range=(0.0, state.left_ny),
            constrain="domain",
            scaleanchor="y",
            scaleratio=1,
            row=2,
            col=1,
        )

        # right
        if state.selectedRepresentation == "Heatmap":
            self.create_heatmap(fig, self._right_data, self._right_mask, 2, 4)
        elif state.selectedRepresentation == "Contours":
            self.create_contour(fig, self._right_data, 2, 4)
        else:
            self.create_combined(fig, self._right_data, self._right_mask, 2, 4)
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
        fig.update_coloraxes(
            colorbar={
                "orientation": "h",
                "lenmode": "fraction",
                "len": 0.6,
                "thickness": 30,
                "y": -0.25,
            }
        )

        self.server.controller.plotly_view_update(fig)

        return fig

    def update_cg2_view(self, **kwargs):
        state = self.server.state

        fig = make_subplots(
            rows=1,
            cols=1,
            specs=[[{"rowspan": 1, "colspan": 1}]],
            print_grid=False,
        )
        # center (1,1)

        # center
        if state.selectedRepresentation == "Heatmap":
            self.create_heatmap(fig, self._center_data, self._center_mask, 1, 1)
        elif state.selectedRepresentation == "Contours":
            self.create_contour(fig, self._center_data, 1, 1)
        else:
            self.create_combined(fig, self._center_data, self._center_mask, 1, 1)
        fig.update_yaxes(
            range=(0.0, state.center_nx),
            constrain="domain",
            scaleanchor="x",
            scaleratio=state.pixel_ratio,
            row=1,
            col=1,
        )
        fig.update_xaxes(
            range=(0.0, state.center_ny), constrain="domain", scaleratio=2, row=1, col=1
        )
        fig.update_layout(
            coloraxis=dict(colorscale=state.selectedColor), showlegend=False
        )
        fig.update_coloraxes(
            colorbar={
                "orientation": "h",
                "lenmode": "fraction",
                "len": 0.6,
                "thickness": 30,
                "y": -0.25,
            }
        )

        self.server.controller.plotly_view_update(fig)

        return fig

    def create_heatmap(self, fig, data, mask, _row, _col, **kwargs):
        state = self.server.state
        fig.add_trace(
            go.Heatmap(
                z=data,
                opacity=1.0,
                coloraxis="coloraxis",
            ),
            row=_row,
            col=_col,
        )
        if state.show_mask:
            fig.append_trace(
                go.Heatmap(
                    z=mask,
                    opacity=1.0,
                    colorscale=[[0, "rgb(0,0,0)"], [1, "rgb(0,0,0)"]],
                    showlegend=False,
                    showscale=False,
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

    def create_combined(self, fig, data, mask, _row, _col, **kwargs):
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
        if state.show_mask:
            fig.append_trace(
                go.Heatmap(
                    z=mask,
                    opacity=1.0,
                    colorscale=[[0, "rgb(0,0,0)"], [1, "rgb(0,0,0)"]],
                    showlegend=False,
                    showscale=False,
                ),
                row=_row,
                col=_col,
            )
