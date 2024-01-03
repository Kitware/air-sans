from trame.assets.local import LocalFileManager

ASSETS = LocalFileManager(__file__)

ASSETS.url("plotly", "./plotly.png")
ASSETS.url("vtk", "./vtk.png")
