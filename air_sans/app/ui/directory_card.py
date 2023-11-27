from trame.widgets import html, vuetify

from . import base_card as bc


def on_click(e):
    print(e)


def directory_card(ctrl):
    with bc.ui_card(
        "directory_workflow",
    ):
        bc.ui_card_title(
            title="Directory",
            ui_icon="mdi-folder-eye-outline",
        )
        with bc.ui_card_text():
            directory_card_text(ctrl)


def directory_card_text(ctrl):
    with vuetify.VRow(classes="pa-0 pt-1", dense=True):
        with vuetify.VCol(cols="1"):
            directory_dialog(ctrl)
        with vuetify.VCol(cols="11"):
            vuetify.VTextField(
                classes="mb-1",
                dense=True,
                hide_details=True,
                readonly=True,
                outlined=True,
                disabled=True,
                type="string",
                v_model=("directory_label",),
            )


def directory_dialog(ctrl):
    with vuetify.VDialog(
        v_model=("directory_dialog", False), persistent=True, max_width="300px"
    ):
        with vuetify.Template(
            v_slot_activator="{ on, attrs }",
        ):
            with vuetify.VBtn(
                small=True,
                color="primary",
                dark=True,
                icon=True,
                v_bind="attrs",
                v_on="on",
            ):
                vuetify.VIcon("mdi-folder")
        with vuetify.VCard(
            classes="ma-1 rounded elevation-8",
        ):
            with vuetify.VCardTitle(
                classes="grey lighten-1 pa-0 grey--text text--darken-3",
                style="user-select: none; cursor: pointer",
                hide_details=True,
                dense=True,
            ):
                html.Div("Directory")
            with vuetify.VCardText(classes="pa-1"):
                vuetify.VTreeview(
                    classes="mb-1",
                    dense=True,
                    hide_details=True,
                    v_model=("dirtree",),
                    items=("dirs",),
                    activatable=True,
                    item_key="path",
                    open_on_click=True,
                    update_active=(
                        ctrl.trigger_directory_selection,
                        "[$event]",
                    ),
                )
            with vuetify.VCardActions(
                classes="px-0 py-1",
                hide_details=True,
                dense=True,
            ):
                vuetify.VSpacer()
                with vuetify.VBtn(
                    classes="ma-0",
                    icon=True,
                    dense=True,
                    small=True,
                    tile=True,
                    color="error",
                    click="directory_dialog = false",
                ):
                    vuetify.VIcon("mdi-cancel")
                with vuetify.VBtn(
                    classes="ma-0",
                    icon=True,
                    dense=True,
                    small=True,
                    tile=True,
                    color="success",
                    click="directory_dialog = false",
                ):
                    vuetify.VIcon("mdi-check")
