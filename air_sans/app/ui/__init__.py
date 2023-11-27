from trame.ui.vuetify import SinglePageWithDrawerLayout
from trame.widgets import vuetify, plotly, trame

from air_sans.widgets import air_sans as my_widgets

from . import workflow_buttons as wb
from . import device_card as devc
from . import directory_card as dc
from . import browse_card as bc
from . import scattering_files_card as sfc
from . import transmission_files_card as tfc
from . import image_card as ic


def initialize(server):
    ctrl = server.controller

    with SinglePageWithDrawerLayout(server) as layout:
        # Toolbar
        layout.title.set_text("<strong>AIR-SANS</strong>")
        with layout.icon:
            vuetify.VIcon("mdi-bullseye")
        with layout.toolbar:
            vuetify.VSpacer()
            wb.workflow_buttons()
            vuetify.VSpacer()
            my_widgets.CustomWidget(
                attribute_name="Hello",
                py_attr_name="World",
                click=ctrl.widget_click,
                change=ctrl.widget_change,
            )
            vuetify.VSpacer()
            vuetify.VSlider(  # Add slider
                v_model=("resolution", 6),  # bind variable with an initial value of 6
                min=3,
                max=60,  # slider range
                dense=True,
                hide_details=True,  # presentation setup
            )
            with vuetify.VBtn(icon=True, click=ctrl.reset_camera):
                vuetify.VIcon("mdi-crop-free")
            with vuetify.VBtn(icon=True, click=ctrl.reset_resolution):
                vuetify.VIcon("mdi-undo")
        with layout.drawer as drawer:
            drawer.width = 350
            devc.device_card(ctrl)
            dc.directory_card(ctrl)
            bc.browse_card(ctrl)
            sfc.scattering_files_card(ctrl)
            tfc.transmission_files_card(ctrl)
            ic.image_card(ctrl)
        # Main content
        with layout.content:
            with vuetify.VContainer(
                fluid=True,
                classes="pa-0 fill-height",
                v_show=("selectedDevice",),
            ):
                with trame.SizeObserver("d11_size"):
                    ctrl.update_d11 = plotly.Figure(
                        display_mode_bar=("false",),
                    ).update

        # Footer
        # layout.footer.hide()
