from trame.widgets import html, vuetify

from . import base_card as bc


def on_click(e):
    print(e)


def transmission_files_card(ctrl):
    with bc.ui_card(
        "transmission_workflow",
    ):
        bc.ui_card_title(
            title="transmission",
            ui_icon="mdi-transfer",
        )
        with bc.ui_card_text():
            transmission_files_card_text(ctrl)


def transmission_files_card_text(ctrl):
    html.Div("<strong>Samples</strong>")
    vuetify.VDivider(classes="mb-2")
    sample_files()
    html.Div("<strong>Empty Cell</strong>")
    vuetify.VDivider(classes="mb-2")
    empty_cell_files()
    html.Div("<strong>Direct Beam</strong>")
    vuetify.VDivider(classes="mb-2")
    direct_beam_files()


def sample_files():
    with vuetify.VRow(classes="pa-0 pt-2", dense=True):
        with vuetify.VCombobox(
            classes="mt=2",
            v_model=("transmission_samples_28m",),
            items=("files",),
            label="28 m",
            dense=True,
            hide_details=True,
            hide_no_data=True,
            hide_selected=True,
            chips=True,
            clearable=True,
            multiple=True,
            density="comfortable",
            outlined=True,
        ):
            with vuetify.Template(
                v_slot_selection="{ attrs, item, select, selected }",
            ):
                with vuetify.VChip(
                    v_bind="attrs",
                    input_value="selected",
                    close=True,
                    click="select",
                    click_close="transmission_samples_28m.splice(transmission_samples_28m.indexOf(item), 1);",
                ):
                    html.Div("<strong>{{ item }}</strong>")
    with vuetify.VRow(classes="pa-0", dense=True):
        with vuetify.VCombobox(
            classes="mt=4",
            v_model=("transmission_samples_8m",),
            items=("files",),
            label="8 m",
            dense=True,
            hide_details=True,
            hide_no_data=True,
            hide_selected=True,
            chips=True,
            clearable=True,
            multiple=True,
            density="comfortable",
            outlined=True,
        ):
            with vuetify.Template(
                v_slot_selection="{ attrs, item, select, selected }",
            ):
                with vuetify.VChip(
                    v_bind="attrs",
                    input_value="selected",
                    close=True,
                    click="select",
                    click_close="transmission_samples_8m.splice(transmission_samples_8m.indexOf(item), 1);",
                ):
                    html.Div("<strong>{{ item }}</strong>")
    with vuetify.VRow(classes="pa-0 pb-2", dense=True):
        with vuetify.VCombobox(
            v_model=("transmission_samples_2m",),
            items=("files",),
            label="2 m",
            dense=True,
            hide_details=True,
            hide_no_data=True,
            hide_selected=True,
            chips=True,
            clearable=True,
            multiple=True,
            density="comfortable",
            outlined=True,
        ):
            with vuetify.Template(
                v_slot_selection="{ attrs, item, select, selected }",
            ):
                with vuetify.VChip(
                    v_bind="attrs",
                    input_value="selected",
                    dense=True,
                    close=True,
                    click="select",
                    click_close="transmission_samples_2m.splice(transmission_samples_2m.indexOf(item), 1);",
                ):
                    html.Div("<strong>{{ item }}</strong>")


def empty_cell_files():
    with vuetify.VRow(classes="pa-0 pt-2", dense=True):
        with vuetify.VCombobox(
            classes="mt=2",
            v_model=("transmission_empty_cell_28m",),
            items=("files",),
            label="28 m",
            dense=True,
            hide_details=True,
            hide_no_data=True,
            hide_selected=True,
            chips=True,
            clearable=True,
            multiple=True,
            density="comfortable",
            outlined=True,
        ):
            with vuetify.Template(
                v_slot_selection="{ attrs, item, select, selected }",
            ):
                with vuetify.VChip(
                    v_bind="attrs",
                    input_value="selected",
                    close=True,
                    click="select",
                    click_close="transmission_empty_cell_28m.splice(transmission_empty_cell_28m.indexOf(item), 1);",
                ):
                    html.Div("<strong>{{ item }}</strong>")
    with vuetify.VRow(classes="pa-0", dense=True):
        with vuetify.VCombobox(
            classes="mt=4",
            v_model=("transmission_empty_cell_8m",),
            items=("files",),
            label="8 m",
            dense=True,
            hide_details=True,
            hide_no_data=True,
            hide_selected=True,
            chips=True,
            clearable=True,
            multiple=True,
            density="comfortable",
            outlined=True,
        ):
            with vuetify.Template(
                v_slot_selection="{ attrs, item, select, selected }",
            ):
                with vuetify.VChip(
                    v_bind="attrs",
                    input_value="selected",
                    close=True,
                    click="select",
                    click_close="transmission_empty_cell_8m.splice(transmission_empty_cell_8m.indexOf(item), 1);",
                ):
                    html.Div("<strong>{{ item }}</strong>")
    with vuetify.VRow(classes="pa-0 pb-2", dense=True):
        with vuetify.VCombobox(
            v_model=("transmission_empty_cell_2m",),
            items=("files",),
            label="2 m",
            dense=True,
            hide_details=True,
            hide_no_data=True,
            hide_selected=True,
            chips=True,
            clearable=True,
            multiple=True,
            density="comfortable",
            outlined=True,
        ):
            with vuetify.Template(
                v_slot_selection="{ attrs, item, select, selected }",
            ):
                with vuetify.VChip(
                    v_bind="attrs",
                    input_value="selected",
                    dense=True,
                    close=True,
                    click="select",
                    click_close="transmission_empty_cell_2m.splice(transmission_empty_cell_2m.indexOf(item), 1);",
                ):
                    html.Div("<strong>{{ item }}</strong>")


def direct_beam_files():
    with vuetify.VRow(classes="pa-0 pt-2", dense=True):
        with vuetify.VCombobox(
            classes="mt=2",
            v_model=("transmission_direct_beam_28m",),
            items=("files",),
            label="28 m",
            dense=True,
            hide_details=True,
            hide_no_data=True,
            hide_selected=True,
            chips=True,
            clearable=True,
            multiple=True,
            density="comfortable",
            outlined=True,
        ):
            with vuetify.Template(
                v_slot_selection="{ attrs, item, select, selected }",
            ):
                with vuetify.VChip(
                    v_bind="attrs",
                    input_value="selected",
                    close=True,
                    click="select",
                    click_close="transmission_direct_beam_28m.splice(transmission_direct_beam_28m.indexOf(item), 1);",
                ):
                    html.Div("<strong>{{ item }}</strong>")
    with vuetify.VRow(classes="pa-0", dense=True):
        with vuetify.VCombobox(
            classes="mt=4",
            v_model=("transmission_direct_beam_8m",),
            items=("files",),
            label="8 m",
            dense=True,
            hide_details=True,
            hide_no_data=True,
            hide_selected=True,
            chips=True,
            clearable=True,
            multiple=True,
            density="comfortable",
            outlined=True,
        ):
            with vuetify.Template(
                v_slot_selection="{ attrs, item, select, selected }",
            ):
                with vuetify.VChip(
                    v_bind="attrs",
                    input_value="selected",
                    close=True,
                    click="select",
                    click_close="transmission_direct_beam_8m.splice(transmission_direct_beam_8m.indexOf(item), 1);",
                ):
                    html.Div("<strong>{{ item }}</strong>")
    with vuetify.VRow(classes="pa-0 pb-2", dense=True):
        with vuetify.VCombobox(
            v_model=("transmission_direct_beam_2m",),
            items=("files",),
            label="2 m",
            dense=True,
            hide_details=True,
            hide_no_data=True,
            hide_selected=True,
            chips=True,
            clearable=True,
            multiple=True,
            density="comfortable",
            outlined=True,
        ):
            with vuetify.Template(
                v_slot_selection="{ attrs, item, select, selected }",
            ):
                with vuetify.VChip(
                    v_bind="attrs",
                    input_value="selected",
                    dense=True,
                    close=True,
                    click="select",
                    click_close="transmission_direct_beam_2m.splice(transmission_direct_beam_2m.indexOf(item), 1);",
                ):
                    html.Div("<strong>{{ item }}</strong>")
