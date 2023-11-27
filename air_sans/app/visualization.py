import plotly.graph_objects as go
from plotly.subplots import make_subplots


class Visualization:
    def __init__(self, server):
        self._server = server
        self._state = server.state
        self._ctrl = server.controller
        self._left_data = None
        self._center_data = None
        self._right_data = None

    def set_left_data(self, data):
        self._left_data = data

    def set_center_data(self, data):
        self._center_data = data

    def set_right_data(self, data):
        self._right_data = data

    def create_d11_fig(self, width=100, height=100, **kwargs):
        state = self._state
        print("contour ", width, height)

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
            print_grid=True,
        )
        # center (1,2), left (2,1), right (2,4)
        if state.selectedRepresentation == "Heatmap":
            self.create_heatmap(fig, self._center_data, 1, 2)
        elif state.selectedRepresentation == "Contour":
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
        elif state.selectedRepresentation == "Contour":
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
        elif state.selectedRepresentation == "Contour":
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
        state = self._state

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
        state = self._state

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

    def create_left_contour_fig(self, width=100, height=100, **kwargs):
        state = self._state
        print("contour ", width, height)

        fig = go.Figure(
            data=go.Contour(
                z=self._left_data,
                contours={
                    "coloring": "heatmap",
                    "showlabels": True,
                    "labelfont": {
                        "size": 12,
                        "color": "black",
                    },
                },
                line_smoothing=1,
                coloraxis="coloraxis",
            )
        )
        fig.update_layout(
            # title = 'Mic Patterns',
            # margin=dict(l=20, r=20, t=20, b=20),
            showlegend=False,
            # width=width,
            # height=height,
        )
        fig.update(layout_coloraxis_showscale=False)
        fig.update_yaxes(
            range=(0.0, state.left_nx),
            constrain="domain",
        )
        fig.update_xaxes(
            range=(0.0, state.left_ny),
            constrain="domain",
            scaleanchor="y",
            scaleratio=state.pixel_ratio,
        )
        return fig

    def create_center_contour_fig(self, width=100, height=100, **kwargs):
        state = self._state
        print("contour ", width, height)

        fig = go.Figure(
            data=go.Contour(
                z=self._center_data,
                contours={
                    "coloring": "heatmap",
                    "showlabels": True,
                    "labelfont": {
                        "size": 12,
                        "color": "black",
                    },
                },
                line_smoothing=1,
                coloraxis="coloraxis",
            )
        )
        fig.update_layout(
            # title = 'Mic Patterns',
            # margin=dict(l=20, r=20, t=20, b=20),
            showlegend=False,
            # width=width,
            # height=height,
        )
        fig.update(layout_coloraxis_showscale=False)
        fig.update_yaxes(
            range=(0.0, state.center_nx),
            constrain="domain",
            scaleanchor="x",
            scaleratio=state.pixel_ratio,
        )
        fig.update_xaxes(
            range=(0.0, state.center_ny),
            constrain="domain",
        )
        return fig

    def create_right_contour_fig(self, width=100, height=100, **kwargs):
        state = self._state
        print("contour ", width, height)

        fig = go.Figure(
            data=go.Contour(
                z=self._right_data,
                contours={
                    "coloring": "heatmap",
                    "showlabels": True,
                    "labelfont": {
                        "size": 12,
                        "color": "black",
                    },
                },
                line_smoothing=1,
                coloraxis="coloraxis",
            )
        )
        fig.update_layout(
            # title = 'Mic Patterns',
            # margin=dict(l=20, r=20, t=20, b=20),
            showlegend=False,
            # width=width,
            # height=height,
        )
        fig.update(layout_coloraxis_showscale=False)
        fig.update_yaxes(
            range=(0.0, state.right_nx),
            constrain="domain",
        )
        fig.update_xaxes(
            range=(0.0, state.right_ny),
            constrain="domain",
            scaleanchor="y",
            scaleratio=state.pixel_ratio,
        )
        return fig


def create_visualization(server=None):
    return Visualization(server)
