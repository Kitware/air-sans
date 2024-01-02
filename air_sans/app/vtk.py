from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.numpy_interface.dataset_adapter import numpyTovtkDataArray as np2da
from vtkmodules.vtkRenderingCore import (
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkActor,
    vtkDiscretizableColorTransferFunction,
)
from vtkmodules.vtkFiltersCore import (
    vtkCellDataToPointData,
    vtkContourFilter,
)
from vtkmodules.vtkRenderingAnnotation import (
    vtkScalarBarActor,
    vtkCubeAxesActor,
)

# VTK factory initialization
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleImage  # noqa
import vtkmodules.vtkRenderingOpenGL2  # noqa

from trame.decorators import TrameApp, change


def to_linear_value(v, data_range):
    return v * (data_range[1] - data_range[0]) + data_range[0]


def spectral(ctf, data_range):
    ctf.RemoveAllPoints()

    ctf.SetColorSpaceToRGB()
    ctf.SetScaleToLinear()

    ctf.SetNanColor(0.0, 0.0, 0.0)

    ctf.AddRGBPoint(
        to_linear_value(0 / (11 - 1), data_range),
        158.0 / 255.0,
        1.0 / 255.0,
        66.0 / 255.0,
    )
    ctf.AddRGBPoint(
        to_linear_value(1 / (11 - 1), data_range),
        213.0 / 255.0,
        62.0 / 255.0,
        79.0 / 255.0,
    )
    ctf.AddRGBPoint(
        to_linear_value(2 / (11 - 1), data_range),
        244.0 / 255.0,
        109.0 / 255.0,
        67.0 / 255.0,
    )
    ctf.AddRGBPoint(
        to_linear_value(3 / (11 - 1), data_range),
        253.0 / 255.0,
        174.0 / 255.0,
        97.0 / 255.0,
    )
    ctf.AddRGBPoint(
        to_linear_value(4 / (11 - 1), data_range),
        254.0 / 255.0,
        224.0 / 255.0,
        139.0 / 255.0,
    )
    ctf.AddRGBPoint(
        to_linear_value(5 / (11 - 1), data_range),
        255.0 / 255.0,
        255.0 / 255.0,
        191.0 / 255.0,
    )
    ctf.AddRGBPoint(
        to_linear_value(6 / (11 - 1), data_range),
        230.0 / 255.0,
        245.0 / 255.0,
        152.0 / 255.0,
    )
    ctf.AddRGBPoint(
        to_linear_value(7 / (11 - 1), data_range),
        171.0 / 255.0,
        221.0 / 255.0,
        164.0 / 255.0,
    )
    ctf.AddRGBPoint(
        to_linear_value(8 / (11 - 1), data_range),
        102.0 / 255.0,
        194.0 / 255.0,
        165.0 / 255.0,
    )
    ctf.AddRGBPoint(
        to_linear_value(9 / (11 - 1), data_range),
        50.0 / 255.0,
        136.0 / 255.0,
        189.0 / 255.0,
    )
    ctf.AddRGBPoint(
        to_linear_value(10 / (11 - 1), data_range),
        94.0 / 255.0,
        79.0 / 255.0,
        162.0 / 255.0,
    )
    ctf.SetNumberOfValues(11)
    ctf.DiscretizeOff()

    ctf.Build()

    return ctf


def rdbu(ctf, data_range):
    ctf.RemoveAllPoints()

    ctf.SetColorSpaceToRGB()
    ctf.SetScaleToLinear()

    ctf.SetNanColor(0.0, 0.0, 0.0)

    ctf.AddRGBPoint(
        to_linear_value(0 / (11 - 1), data_range),
        103.0 / 255.0,
        0.0 / 255.0,
        31.0 / 255.0,
    )
    ctf.AddRGBPoint(
        to_linear_value(1 / (11 - 1), data_range),
        178.0 / 255.0,
        24.0 / 255.0,
        43.0 / 255.0,
    )
    ctf.AddRGBPoint(
        to_linear_value(2 / (11 - 1), data_range),
        214.0 / 255.0,
        96.0 / 255.0,
        77.0 / 255.0,
    )
    ctf.AddRGBPoint(
        to_linear_value(3 / (11 - 1), data_range),
        244.0 / 255.0,
        165.0 / 255.0,
        130.0 / 255.0,
    )
    ctf.AddRGBPoint(
        to_linear_value(4 / (11 - 1), data_range),
        253.0 / 255.0,
        219.0 / 255.0,
        199.0 / 255.0,
    )
    ctf.AddRGBPoint(
        to_linear_value(5 / (11 - 1), data_range),
        247.0 / 255.0,
        247.0 / 255.0,
        247.0 / 255.0,
    )
    ctf.AddRGBPoint(
        to_linear_value(6 / (11 - 1), data_range),
        209.0 / 255.0,
        229.0 / 255.0,
        240.0 / 255.0,
    )
    ctf.AddRGBPoint(
        to_linear_value(7 / (11 - 1), data_range),
        146.0 / 255.0,
        197.0 / 255.0,
        222.0 / 255.0,
    )
    ctf.AddRGBPoint(
        to_linear_value(8 / (11 - 1), data_range),
        67.0 / 255.0,
        147.0 / 255.0,
        195.0 / 255.0,
    )
    ctf.AddRGBPoint(
        to_linear_value(9 / (11 - 1), data_range),
        33.0 / 255.0,
        102.0 / 255.0,
        172.0 / 255.0,
    )
    ctf.AddRGBPoint(
        to_linear_value(10 / (11 - 1), data_range),
        5.0 / 255.0,
        48.0 / 255.0,
        97.0 / 255.0,
    )
    ctf.SetNumberOfValues(11)
    ctf.DiscretizeOff()

    ctf.Build()

    return ctf


def gray(ctf, data_range):
    ctf.RemoveAllPoints()

    ctf.SetColorSpaceToRGB()
    ctf.SetScaleToLinear()

    ctf.SetNanColor(0.0, 0.5, 1.0)

    ctf.AddRGBPoint(
        to_linear_value(0 / (9 - 1), data_range),
        255.0 / 255.0,
        255.0 / 255.0,
        255.0 / 255.0,
    )
    ctf.AddRGBPoint(
        to_linear_value(1 / (9 - 1), data_range),
        240.0 / 255.0,
        240.0 / 255.0,
        240.0 / 255.0,
    )
    ctf.AddRGBPoint(
        to_linear_value(2 / (9 - 1), data_range),
        217.0 / 255.0,
        217.0 / 255.0,
        217.0 / 255.0,
    )
    ctf.AddRGBPoint(
        to_linear_value(3 / (9 - 1), data_range),
        189.0 / 255.0,
        189.0 / 255.0,
        189.0 / 255.0,
    )
    ctf.AddRGBPoint(
        to_linear_value(4 / (9 - 1), data_range),
        150.0 / 255.0,
        150.0 / 255.0,
        150.0 / 255.0,
    )
    ctf.AddRGBPoint(
        to_linear_value(5 / (9 - 1), data_range),
        115.0 / 255.0,
        115.0 / 255.0,
        115.0 / 255.0,
    )
    ctf.AddRGBPoint(
        to_linear_value(6 / (9 - 1), data_range),
        82.0 / 255.0,
        82.0 / 255.0,
        82.0 / 255.0,
    )
    ctf.AddRGBPoint(
        to_linear_value(7 / (9 - 1), data_range),
        37.0 / 255.0,
        37.0 / 255.0,
        37.0 / 255.0,
    )
    ctf.AddRGBPoint(
        to_linear_value(8 / (9 - 1), data_range), 0.0 / 255.0, 0.0 / 255.0, 0.0 / 255.0
    )
    ctf.SetNumberOfValues(9)
    ctf.DiscretizeOff()

    ctf.Build()

    return ctf


def ylgn(ctf, data_range):
    ctf.RemoveAllPoints()

    ctf.SetColorSpaceToRGB()
    ctf.SetScaleToLinear()

    ctf.SetNanColor(1.0, 0.5, 0.0)

    ctf.AddRGBPoint(
        to_linear_value(0 / (9 - 1), data_range),
        255.0 / 255.0,
        255.0 / 255.0,
        229.0 / 255.0,
    )
    ctf.AddRGBPoint(
        to_linear_value(1 / (9 - 1), data_range),
        247.0 / 255.0,
        252.0 / 255.0,
        185.0 / 255.0,
    )
    ctf.AddRGBPoint(
        to_linear_value(2 / (9 - 1), data_range),
        217.0 / 255.0,
        240.0 / 255.0,
        163.0 / 255.0,
    )
    ctf.AddRGBPoint(
        to_linear_value(3 / (9 - 1), data_range),
        173.0 / 255.0,
        221.0 / 255.0,
        142.0 / 255.0,
    )
    ctf.AddRGBPoint(
        to_linear_value(4 / (9 - 1), data_range),
        120.0 / 255.0,
        198.0 / 255.0,
        121.0 / 255.0,
    )
    ctf.AddRGBPoint(
        to_linear_value(5 / (9 - 1), data_range),
        65.0 / 255.0,
        171.0 / 255.0,
        93.0 / 255.0,
    )
    ctf.AddRGBPoint(
        to_linear_value(6 / (9 - 1), data_range),
        35.0 / 255.0,
        132.0 / 255.0,
        67.0 / 255.0,
    )
    ctf.AddRGBPoint(
        to_linear_value(7 / (9 - 1), data_range),
        0.0 / 255.0,
        104.0 / 255.0,
        55.0 / 255.0,
    )
    ctf.AddRGBPoint(
        to_linear_value(8 / (9 - 1), data_range),
        0.0 / 255.0,
        69.0 / 255.0,
        41.0 / 255.0,
    )
    ctf.SetNumberOfValues(9)
    ctf.DiscretizeOff()

    ctf.Build()

    return ctf


def ylorbr(ctf, data_range):
    ctf.RemoveAllPoints()

    ctf.SetColorSpaceToRGB()
    ctf.SetScaleToLinear()

    ctf.SetNanColor(0.0, 0.5, 1.0)

    ctf.AddRGBPoint(
        to_linear_value(0 / (9 - 1), data_range),
        255.0 / 255.0,
        255.0 / 255.0,
        229.0 / 255.0,
    )
    ctf.AddRGBPoint(
        to_linear_value(1 / (9 - 1), data_range),
        255.0 / 255.0,
        247.0 / 255.0,
        188.0 / 255.0,
    )
    ctf.AddRGBPoint(
        to_linear_value(2 / (9 - 1), data_range),
        254.0 / 255.0,
        227.0 / 255.0,
        145.0 / 255.0,
    )
    ctf.AddRGBPoint(
        to_linear_value(3 / (9 - 1), data_range),
        254.0 / 255.0,
        196.0 / 255.0,
        79.0 / 255.0,
    )
    ctf.AddRGBPoint(
        to_linear_value(4 / (9 - 1), data_range),
        254.0 / 255.0,
        153.0 / 255.0,
        41.0 / 255.0,
    )
    ctf.AddRGBPoint(
        to_linear_value(5 / (9 - 1), data_range),
        236.0 / 255.0,
        112.0 / 255.0,
        20.0 / 255.0,
    )
    ctf.AddRGBPoint(
        to_linear_value(6 / (9 - 1), data_range),
        204.0 / 255.0,
        76.0 / 255.0,
        2.0 / 255.0,
    )
    ctf.AddRGBPoint(
        to_linear_value(7 / (9 - 1), data_range),
        153.0 / 255.0,
        52.0 / 255.0,
        4.0 / 255.0,
    )
    ctf.AddRGBPoint(
        to_linear_value(8 / (9 - 1), data_range),
        102.0 / 255.0,
        37.0 / 255.0,
        6.0 / 255.0,
    )
    ctf.SetNumberOfValues(9)
    ctf.DiscretizeOff()

    ctf.Build()

    return ctf


LUTS = {
    "spectral": spectral,
    "rdbu": rdbu,
    "gray": gray,
    "ylgn": ylgn,
    "ylorbr": ylorbr,
}


@TrameApp()
class VTKDetectorView:
    def __init__(self, server, show_scalar_bar=False):
        self.server = server

        self.color_range = [0, 1]
        self.lut = vtkDiscretizableColorTransferFunction()

        self.renderer = vtkRenderer()
        self.renderer.SetBackground(1.0, 1.0, 1.0)
        self.render_window = vtkRenderWindow()
        self.render_window.AddRenderer(self.renderer)
        self.render_window.OffScreenRenderingOn()

        self.render_window_interactor = vtkRenderWindowInteractor()
        self.render_window_interactor.SetRenderWindow(self.render_window)
        self.render_window_interactor.SetInteractorStyle(vtkInteractorStyleImage())
        # self.render_window_interactor.GetInteractorStyle().SetCurrentStyleToTrackballCamera()

        # Heatmap
        self.mapper = vtkDataSetMapper()
        self.mapper.SetLookupTable(self.lut)
        self.actor = vtkActor()
        self.actor.SetVisibility(0)
        self.actor.SetMapper(self.mapper)
        self.renderer.AddActor(self.actor)

        lut = vtkLookupTable()
        lut.SetRange(0.0, 1.0)
        lut.SetNanColor(1.0, 0.0, 0.0, 0.0)
        lut.SetRampToLinear()
        lut.SetHueRange(0.0, 0.0)
        lut.SetSaturationRange(0.0, 0.0)
        lut.SetValueRange(0.0, 1.0)

        self.mask_mapper = vtkDataSetMapper()
        self.mask_mapper.SetScalarVisibility(True)
        self.mask_mapper.SetLookupTable(lut)
        self.mask_actor = vtkActor()
        self.mask_actor.SetVisibility(0)
        self.mask_actor.SetMapper(self.mask_mapper)
        self.renderer.AddActor(self.mask_actor)
        # Contour
        self.c2p = vtkCellDataToPointData()
        self.contour = vtkContourFilter()
        self.contour_mapper = vtkPolyDataMapper()
        self.contour_mapper.SetLookupTable(self.lut)
        self.contour_mapper.SetScalarVisibility(True)
        self.contour_actor = vtkActor()
        self.contour_actor.SetVisibility(0)
        self.contour_actor.SetMapper(self.contour_mapper)
        self.contour_actor.GetProperty().SetLineWidth(2)
        self.contour_actor.GetProperty().SetColor(0, 0, 0)
        self.renderer.AddActor(self.contour_actor)

        self.cubeaxes = vtkCubeAxesActor()
        self.cubeaxes.SetCamera(self.renderer.GetActiveCamera())
        font_size = 9
        self.cubeaxes.SetScreenSize(font_size / 12 * 10.0)
        self.cubeaxes.GetXAxesLinesProperty().SetColor(0.0, 0.0, 0.0)
        self.cubeaxes.GetTitleTextProperty(0).SetColor(0.0, 0.0, 0.0)
        self.cubeaxes.GetLabelTextProperty(0).SetColor(0.0, 0.0, 0.0)
        self.cubeaxes.GetYAxesLinesProperty().SetColor(0.0, 0.0, 0.0)
        self.cubeaxes.GetTitleTextProperty(1).SetColor(0.0, 0.0, 0.0)
        self.cubeaxes.GetLabelTextProperty(1).SetColor(0.0, 0.0, 0.0)
        self.cubeaxes.GetZAxesLinesProperty().SetColor(0.0, 0.0, 0.0)
        self.cubeaxes.GetTitleTextProperty(2).SetColor(0.0, 0.0, 0.0)
        self.cubeaxes.GetLabelTextProperty(2).SetColor(0.0, 0.0, 0.0)
        self.cubeaxes.SetXTitle("")
        self.cubeaxes.SetYTitle("")
        self.cubeaxes.SetZTitle("")
        self.cubeaxes.SetTickLocation(1)
        self.renderer.AddActor(self.cubeaxes)

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
            self.scalar_bar.GetLabelTextProperty().SetColor(0.0, 0.0, 0.0)
            self.scalar_bar.GetLabelTextProperty().SetFontSize(font_size)
            self.scalar_bar.GetLabelTextProperty().BoldOff()
            self.scalar_bar.GetLabelTextProperty().ItalicOff()
            self.scalar_bar.GetLabelTextProperty().ShadowOff()
            self.scalar_bar.SetUnconstrainedFontSize(True)
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

    def set_data_minmax(self, data_min, data_max):
        self.color_range = [data_min, data_max]

    def update_data(self, np_array, mask, x, y):
        state = self.server.state

        self.image_data = vtkImageData()
        self.image_data.SetSpacing(x, y, 1)

        self.image_data.SetDimensions(np_array.shape[1] + 1, np_array.shape[0] + 1, 1)

        vtk_array = np2da(np_array.flatten(), name="scalar")
        self.image_data.GetCellData().SetScalars(vtk_array)

        self.mask_data = vtkImageData()
        self.mask_data.SetSpacing(x, y, 1)

        self.mask_data.SetDimensions(mask.shape[1] + 1, mask.shape[0] + 1, 1)

        vtk_mask = np2da(mask.flatten(), name="scalar")
        self.mask_data.GetCellData().SetScalars(vtk_mask)

        # self.color_range = vtk_array.GetRange()
        self.update_lut()

        # Heatmap
        if state.selectedRepresentation == "Heatmap":
            self.mapper.SetScalarRange(self.color_range)
            self.mapper.SetInputData(self.image_data)
            self.actor.SetVisibility(1)
            if state.show_mask:
                self.mask_mapper.SetInputData(self.mask_data)
                self.mask_actor.SetVisibility(1)
            else:
                self.mask_actor.SetVisibility(0)
            self.contour_actor.SetVisibility(0)
        # Contours
        elif state.selectedRepresentation == "Contours":
            self.c2p.SetInputData(self.image_data)
            self.c2p.Update()
            self.contour.SetInputData(self.c2p.GetOutput())
            self.contour.SetArrayComponent(0)
            self.contour.GenerateValues(10, self.color_range)
            self.contour.Update()
            self.contour_mapper.SetInputConnection(self.contour.GetOutputPort())
            self.contour_mapper.SetScalarVisibility(True)
            self.contour_mapper.SetScalarRange(self.color_range)
            self.contour_actor.SetVisibility(1)
            self.actor.SetVisibility(0)
            self.mask_actor.SetVisibility(0)
        else:
            self.mapper.SetScalarRange(self.color_range)
            self.mapper.SetInputData(self.image_data)
            self.actor.SetVisibility(1)
            if state.show_mask:
                self.mask_mapper.SetInputData(self.mask_data)
                self.mask_actor.SetVisibility(1)
            else:
                self.mask_actor.SetVisibility(0)
            self.c2p.SetInputData(self.image_data)
            self.c2p.Update()
            self.contour.SetInputData(self.c2p.GetOutput())
            self.contour.SetArrayComponent(0)
            self.contour.GenerateValues(10, self.color_range)
            self.contour.Update()
            self.contour_mapper.SetInputConnection(self.contour.GetOutputPort())
            self.contour_mapper.SetScalarRange(self.color_range)
            self.contour_mapper.SetScalarVisibility(False)
            self.contour_actor.SetVisibility(1)

        if state.show_mask and state.selectedRepresentation != "Contours":
            self.cubeaxes.SetBounds(self.mask_data.GetBounds())
        else:
            self.cubeaxes.SetBounds(self.image_data.GetBounds())

        if self.html_reset_camera:
            self.html_reset_camera()
            self.html_update()
