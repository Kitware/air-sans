from trame.widgets import vuetify

from . import base_card as bc


def image_card(ctrl):
    with bc.ui_card(
        "image_workflow",
    ):
        bc.ui_card_title(
            title="Image",
            ui_icon="mdi-image-multiple-outline",
        )
        with bc.ui_card_text():
            image_card_text(ctrl)


def image_card_text(ctrl):
    with vuetify.VRow(classes="pa-0 pt-1", dense=True, hide_details=True):
        with vuetify.VCol(cols="6"):
            vuetify.VSelect(
                v_model=("selectedRepresentation",),
                items=("representations",),
                label="Representation",
                dense=True,
                hide_details=True,
                outlined=True,
            )
        with vuetify.VCol(cols="6"):
            vuetify.VSelect(
                v_model=("selectedColor",),
                items=("colors",),
                label="Colors",
                dense=True,
                hide_details=True,
                outlined=True,
            )
    with vuetify.VRow(classes="pa-0 pt-1", dense=True, hide_details=True):
        with vuetify.VCol(cols="6"):
            vuetify.VCheckbox(
                v_model=("contour_labels",),
                label="Contour labels",
                dense=True,
                hide_details=True,
            )
