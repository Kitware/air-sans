from trame.widgets import vuetify

from . import base_card as bc


def browse_card(ctrl):
    with bc.ui_card(
        "browse_workflow",
    ):
        bc.ui_card_title(
            title="Browse",
            ui_icon="mdi-application-outline",
        )
        with bc.ui_card_text():
            browse_card_text(ctrl)


def browse_card_text(ctrl):
    with vuetify.VRow(classes="pa-0 pt-1", dense=True):
        with vuetify.VList(
            dense=True,
            hide_details=True,
        ):
            with vuetify.VListItemGroup(
                v_model=("file_selected",),
                color="primary",
            ):
                with vuetify.VListItem(
                    v_for="(item, index) in files",
                    key="index",
                    dense=True,
                    hide_details=True,
                    click=(ctrl.selected_file, "[item]"),
                    color="primary",
                    style="min-height:10px",
                ):
                    with vuetify.VListItemIcon(classes="ma-0 mr-1"):
                        vuetify.VIcon("mdi-file", x_small=True)
                    with vuetify.VListItemContent(classes="pa-0"):
                        vuetify.VListItemTitle("{{item}}")
