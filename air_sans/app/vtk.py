import pyvista as pv
from vtkmodules.vtkRenderingCore import (
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkDataSetMapper,
    vtkActor,
)
from vtkmodules.vtkRenderingAnnotation import vtkScalarBarActor, vtkCubeAxesActor

# VTK factory initialization
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleImage  # noqa
import vtkmodules.vtkRenderingOpenGL2  # noqa

from trame.decorators import TrameApp, change


@TrameApp()
class DetectorView:
    def __init__(self, server, show_scalar_bar=False):
        self.server = server

        self.lut = pv.LookupTable(server.state.selectedColor)

        self.renderer = vtkRenderer()
        self.render_window = vtkRenderWindow()
        self.render_window.AddRenderer(self.renderer)
        self.render_window.OffScreenRenderingOn()

        self.render_window_interactor = vtkRenderWindowInteractor()
        self.render_window_interactor.SetRenderWindow(self.render_window)
        self.render_window_interactor.SetInteractorStyle(vtkInteractorStyleImage())
        # self.render_window_interactor.GetInteractorStyle().SetCurrentStyleToTrackballCamera()

        self.mapper = vtkDataSetMapper()
        self.mapper.SetLookupTable(self.lut)
        self.actor = vtkActor()
        self.actor.SetVisibility(0)
        self.actor.SetMapper(self.mapper)
        self.renderer.AddActor(self.actor)

        self.grid = vtkCubeAxesActor()
        self.grid.SetCamera(self.renderer.GetActiveCamera())
        self.grid.SetXTitle("")
        self.grid.SetYTitle("")
        self.grid.SetZTitle("")
        self.renderer.AddActor(self.grid)

        self.image_data = None
        self.html_update = None
        self.html_reset_camera = None

        self.scalar_bar = None
        if show_scalar_bar:
            self.scalar_bar = vtkScalarBarActor()
            self.scalar_bar.SetLookupTable(self.lut)
            self.scalar_bar.SetOrientationToHorizontal()
            self.scalar_bar.SetPosition(0, 0)
            self.scalar_bar.SetPosition2(1, 0.1)
            self.renderer.AddActor(self.scalar_bar)

    @change("selectedColor")
    def on_preset_change(self, selectedColor, **kwargs):
        self.lut.apply_cmap(selectedColor)
        self.html_update()

    def set_html_view(self, view):
        self.html_update = view.update
        self.html_reset_camera = view.reset_camera

        if self.image_data:
            self.html_reset_camera()
            self.html_update()

    def update_data(self, np_array, x, y):
        self.image_data = pv.ImageData(
            dimensions=(np_array.shape[1] + 1, np_array.shape[0] + 1, 1),
            spacing=(1, y / x, 1),
        )
        self.image_data.cell_data.set_scalars(np_array.flatten())
        data_range = self.image_data.cell_data.active_scalars.GetRange()
        self.mapper.SetScalarRange(data_range)
        self.mapper.SetInputData(self.image_data)
        self.actor.SetVisibility(1)
        self.grid.SetBounds(self.image_data.GetBounds())

        if self.html_reset_camera:
            self.html_reset_camera()
            self.html_update()
