from trame.widgets import html, vuetify
from .ui_scattering import create_scattering_content
from .ui_transmission import create_transmission_content

SUPPORTED_DEVICES = ["D11+"]


class AbstractCard(vuetify.VCard):
    def __init__(self, key, icon, title):
        super().__init__(
            # classes="mb-3",
            tile=True,
            v_show=f"panel_visible.includes('{key}')",
        )
        with self:
            with vuetify.VCardTitle(
                classes="grey lighten-1 py-0 px-1 grey--text text--darken-3",
                style="user-select: none;",
                hide_details=True,
                dense=True,
            ) as self._title:
                vuetify.VIcon(icon, classes="mr-1", color="grey darken-3")
                html.Div(title)

            self._content = vuetify.VCardText(classes="pa-1")


class DeviceSelector(AbstractCard):
    def __init__(self):
        super().__init__("device", "mdi-microscope", "Device")
        with self._content:
            with vuetify.VRow(classes="px-0 py-1", dense=True, hide_details=True):
                with vuetify.VCol(cols="6"):
                    vuetify.VSelect(
                        v_model=("selectedDevice", None),
                        items=("devices", SUPPORTED_DEVICES),
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


class DirectoryDialog(vuetify.VDialog):
    def __init__(self, select_directory_fn):
        super().__init__(
            v_model=("directory_dialog", False),
            persistent=True,
        )
        with self:
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
                classes="ma-1 rounded elevation-8", style="min-width: 50vw;"
            ):
                with vuetify.VCardTitle(
                    classes="grey lighten-1 px-2 py-0 grey--text text--darken-3",
                    style="user-select: none;",
                    hide_details=True,
                    dense=True,
                ):
                    html.Div("Directory")
                with vuetify.VCardText(
                    classes="pa-1", style="height: 50vh; overflow: auto;"
                ):
                    vuetify.VTreeview(
                        classes="mb-1",
                        dense=True,
                        hide_details=True,
                        v_model=("dirtree", []),
                        items=("dirs", []),
                        activatable=True,
                        item_key="path",
                        open_on_click=True,
                        update_active=(
                            select_directory_fn,
                            "[$event]",
                        ),
                    )
                with vuetify.VCardActions(
                    classes="py-1",
                    hide_details=True,
                    dense=True,
                ):
                    vuetify.VSpacer()
                    with vuetify.VBtn(
                        icon=True,
                        dense=True,
                        small=True,
                        tile=True,
                        color="error",
                        click="directory_dialog = false",
                    ):
                        vuetify.VIcon("mdi-cancel")
                    with vuetify.VBtn(
                        icon=True,
                        dense=True,
                        small=True,
                        tile=True,
                        color="success",
                        click="directory_dialog = false",
                    ):
                        vuetify.VIcon("mdi-check")


class Directory(AbstractCard):
    def __init__(self, select_directory_fn):
        super().__init__("directory", "mdi-folder-eye-outline", "Directory")
        with self._content:
            with vuetify.VRow(classes="px-0 py-1", align_self="center"):
                with vuetify.VCol(cols="1", align_self="center"):
                    DirectoryDialog(select_directory_fn)
                with vuetify.VCol(cols="11"):
                    vuetify.VTextField(
                        classes="mb-1",
                        dense=True,
                        hide_details=True,
                        readonly=True,
                        outlined=True,
                        disabled=True,
                        type="string",
                        v_model=("directory_label", None),
                    )


class FileSelector(AbstractCard):
    def __init__(self, file_selection):
        super().__init__("file", "mdi-application-outline", "Browse")
        with self._content as content:
            content.classes = "px-0 mx-0"
            content.style = "max-height: min(12rem, 40vh); overflow: auto;"
            with vuetify.VList(
                dense=True,
                hide_details=True,
            ):
                with vuetify.VListItemGroup(
                    v_model=("file_selected", None),
                    color="primary",
                ):
                    with vuetify.VListItem(
                        v_for="(item, index) in files",
                        key="index",
                        dense=True,
                        hide_details=True,
                        click=(file_selection, "[item]"),
                        color="primary",
                        style="min-height:10px",
                    ):
                        with vuetify.VListItemIcon(classes="ma-0 mr-1"):
                            vuetify.VIcon("mdi-file", x_small=True)
                        with vuetify.VListItemContent(classes="pa-0"):
                            vuetify.VListItemTitle("{{item}}")


class FigureControl(AbstractCard):
    def __init__(self):
        super().__init__("viz", "mdi-image-multiple-outline", "Image")
        with self._content:
            with vuetify.VRow(classes="pa-0 pt-1", dense=True, hide_details=True):
                with vuetify.VCol(cols="6"):
                    vuetify.VSelect(
                        v_model=("selectedRepresentation", "Heatmap"),
                        items=("representations", ["Heatmap", "Contours", "Combined"]),
                        label="Representation",
                        dense=True,
                        hide_details=True,
                        outlined=True,
                    )
                with vuetify.VCol(cols="6"):
                    vuetify.VSelect(
                        v_model=("selectedColor", "spectral"),
                        items=(
                            "colors",
                            ["spectral", "rdbu", "gray", "blackbody", "sunset"],
                        ),
                        label="Colors",
                        dense=True,
                        hide_details=True,
                        outlined=True,
                    )
            with vuetify.VRow(classes="pa-0 pt-1", dense=True, hide_details=True):
                with vuetify.VCol(cols="6"):
                    vuetify.VCheckbox(
                        v_model=("contour_labels", True),
                        label="Contour labels",
                        dense=True,
                        hide_details=True,
                    )


class Scattering(AbstractCard):
    def __init__(self):
        super().__init__("scattering", "mdi-scatter-plot-outline", "Scattering")
        with self._content:
            create_scattering_content()


class Transmission(AbstractCard):
    def __init__(self):
        super().__init__("transmission", "mdi-transfer", "Transmission")
        with self._content:
            create_transmission_content()
