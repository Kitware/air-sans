# Install app from local directory
pip install wheel # needed to install /local-app
pip install /local-app
pip uninstall -y vtk
pip install --extra-index-url https://wheels.vtk.org vtk-egl