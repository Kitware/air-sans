from trame.widgets import vuetify

from . import base_card as bc


def device_card(ctrl):
    with bc.ui_card(
        "device_workflow",
    ):
        bc.ui_card_title(
            title="Device",
            ui_icon="mdi-microscope",
        )
        with bc.ui_card_text():
            device_card_text(ctrl)


def device_card_text(ctrl):
    with vuetify.VRow(classes="pa-0 pt-1", dense=True, hide_details=True):
        with vuetify.VCol(cols="6"):
            vuetify.VSelect(
                v_model=("selectedDevice",),
                items=("devices",),
                label="Device",
                dense=True,
                hide_details=True,
                outlined=True,
            )
        with vuetify.VCol(cols="6"):
            vuetify.VSelect(
                v_model=("device_active_data", None),
                items=("device_data", ["", "mask", "efficiency", "error"]),
                label="Parameters",
                dense=True,
                hide_details=True,
                outlined=True,
            )
