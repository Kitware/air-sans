from trame.ui.vuetify import SinglePageWithDrawerLayout
from trame.widgets import vuetify, plotly, trame

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
            ):
                with trame.SizeObserver("d11_size"):
                    ctrl.update_d11 = plotly.Figure(
                        display_mode_bar=("false",),
                        v_show=("figure_ready", False),
                    ).update

        # Footer
        # layout.footer.hide()
