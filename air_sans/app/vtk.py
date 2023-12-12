# import pyvista as pv
from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.numpy_interface.dataset_adapter import numpyTovtkDataArray as np2da
from vtkmodules.vtkRenderingCore import (
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkDataSetMapper,
    vtkActor,
    vtkDiscretizableColorTransferFunction,
)
from vtkmodules.vtkRenderingAnnotation import vtkScalarBarActor, vtkCubeAxesActor

# VTK factory initialization
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleImage  # noqa
import vtkmodules.vtkRenderingOpenGL2  # noqa

from trame.decorators import TrameApp, change


def to_linear_value(v, data_range):
    return v * (data_range[1] - data_range[0]) + data_range[0]


def samsel(ctf, data_range):
    ctf.RemoveAllPoints()

    ctf.SetColorSpaceToRGB()
    ctf.SetScaleToLinear()

    ctf.SetNanColor(0.0, 0.0, 0.0)

    ctf.AddRGBPoint(
        to_linear_value(0, data_range), 0.05639999999999999, 0.05639999999999999, 0.47
    )
    ctf.AddRGBPoint(
        to_linear_value(0.17159223942480895, data_range),
        0.24300000000000013,
        0.4603500000000004,
        0.81,
    )
    ctf.AddRGBPoint(
        to_linear_value(0.2984914818394138, data_range),
        0.3568143826543521,
        0.7450246485363142,
        0.954367702893722,
    )
    ctf.AddRGBPoint(
        to_linear_value(0.4321287371255907, data_range),
        0.6882,
        0.93,
        0.9179099999999999,
    )
    ctf.AddRGBPoint(
        to_linear_value(0.5, data_range),
        0.8994959551205902,
        0.944646394975174,
        0.7686567142818399,
    )
    ctf.AddRGBPoint(
        to_linear_value(0.5882260353170073, data_range),
        0.957107977357604,
        0.8338185108985666,
        0.5089156299842102,
    )
    ctf.AddRGBPoint(
        to_linear_value(0.7061412605695164, data_range),
        0.9275207599610714,
        0.6214389091739178,
        0.31535705838676426,
    )
    ctf.AddRGBPoint(
        to_linear_value(0.8476395308725272, data_range),
        0.8,
        0.3520000000000001,
        0.15999999999999998,
    )
    ctf.AddRGBPoint(
        to_linear_value(1, data_range), 0.59, 0.07670000000000013, 0.11947499999999994
    )

    ctf.SetNumberOfValues(9)
    ctf.DiscretizeOff()

    ctf.Build()

    return ctf


def black_body(ctf, data_range):
    ctf.RemoveAllPoints()

    ctf.SetColorSpaceToRGB()
    ctf.SetScaleToLinear()

    ctf.SetNanColor(0.0, 0.498039215686, 1.0)

    ctf.AddRGBPoint(to_linear_value(0.0, data_range), 0.0, 0.0, 0.0)
    ctf.AddRGBPoint(to_linear_value(0.4, data_range), 0.901960784314, 0.0, 0.0)
    ctf.AddRGBPoint(
        to_linear_value(0.8, data_range), 0.901960784314, 0.901960784314, 0.0
    )
    ctf.AddRGBPoint(to_linear_value(1.0, data_range), 1.0, 1.0, 1.0)

    ctf.SetNumberOfValues(4)
    ctf.DiscretizeOff()

    return ctf


def gray(ctf, data_range):
    ctf.RemoveAllPoints()

    ctf.SetColorSpaceToRGB()
    ctf.SetScaleToLinear()

    ctf.SetNanColor(1.0, 0.0, 0.0)

    ctf.AddRGBPoint(to_linear_value(0.0, data_range), 0.0, 0.0, 0.0)
    ctf.AddRGBPoint(to_linear_value(1.0, data_range), 1.0, 1.0, 1.0)

    ctf.SetNumberOfValues(2)
    ctf.DiscretizeOff()

    ctf.Build()

    return ctf


def xray(ctf, data_range):
    ctf.RemoveAllPoints()

    ctf.SetColorSpaceToRGB()
    ctf.SetScaleToLinear()

    ctf.SetNanColor(1.0, 0.0, 0.0)

    ctf.AddRGBPoint(to_linear_value(0.0, data_range), 1.0, 1.0, 1.0)
    ctf.AddRGBPoint(to_linear_value(1.0, data_range), 0.0, 0.0, 0.0)

    ctf.SetNumberOfValues(2)
    ctf.DiscretizeOff()

    ctf.Build()

    return ctf


def cool(ctf, data_range):
    ctf.RemoveAllPoints()

    ctf.SetColorSpaceToRGB()
    ctf.SetScaleToLinear()

    ctf.SetNanColor(1.0, 1.0, 0.0)

    ctf.AddRGBPoint(
        to_linear_value(0.0, data_range), 0.23137254902, 0.298039215686, 0.752941176471
    )
    ctf.AddRGBPoint(to_linear_value(0.5, data_range), 0.865, 0.865, 0.865)
    ctf.AddRGBPoint(
        to_linear_value(1.0, data_range),
        0.705882352941,
        0.0156862745098,
        0.149019607843,
    )

    ctf.SetNumberOfValues(3)
    ctf.DiscretizeOff()

    ctf.Build()

    return ctf


def warm(ctf, data_range):
    ctf.RemoveAllPoints()

    ctf.SetColorSpaceToRGB()
    ctf.SetScaleToLinear()

    ctf.SetNanColor(1.0, 1.0, 0.0)

    ctf.AddRGBPoint(
        to_linear_value(0.0, data_range),
        0.705882352941,
        0.0156862745098,
        0.149019607843,
    )
    ctf.AddRGBPoint(to_linear_value(0.5, data_range), 0.865, 0.865, 0.865)
    ctf.AddRGBPoint(
        to_linear_value(1.0, data_range), 0.23137254902, 0.298039215686, 0.752941176471
    )

    ctf.SetNumberOfValues(3)
    ctf.DiscretizeOff()

    ctf.Build()

    return ctf


LUTS = {
    "samsel": samsel,
    "warm": warm,
    "cool": cool,
    "ray": xray,
    "gray": gray,
    "black body": black_body,
}


@TrameApp()
class DetectorView:
    def __init__(self, server, show_scalar_bar=False):
        self.server = server

        self.color_range = [0, 1]
        self.lut = vtkDiscretizableColorTransferFunction()

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
    def on_preset_change(self, **kwargs):
        self.update_lut()
        self.html_update()

    def set_html_view(self, view):
        self.html_update = view.update
        self.html_reset_camera = view.reset_camera

        if self.image_data:
            self.html_reset_camera()
            self.html_update()

    def update_lut(self):
        LUTS[self.server.state.selectedColor](self.lut, self.color_range)

    def update_data(self, np_array, x, y):
        self.image_data = vtkImageData()
        self.image_data.SetSpacing(1, y / x, 1)
        self.image_data.SetDimensions(np_array.shape[1] + 1, np_array.shape[0] + 1, 1)

        vtk_array = np2da(np_array.flatten(), name="scalar")
        self.image_data.GetCellData().SetScalars(vtk_array)

        self.color_range = vtk_array.GetRange()
        self.update_lut()

        self.mapper.SetScalarRange(self.color_range)
        self.mapper.SetInputData(self.image_data)
        self.actor.SetVisibility(1)
        self.grid.SetBounds(self.image_data.GetBounds())

        if self.html_reset_camera:
            self.html_reset_camera()
            self.html_update()
