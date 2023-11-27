from trame.widgets import vuetify


def workflow_buttons():
    vuetify.VCheckbox(
        v_model=("device_workflow", False),
        color="success",
        on_icon="mdi-microscope",
        off_icon="mdi-microscope",
        classes="mx-1",
        hide_details=True,
        dense=True,
    )
    vuetify.VCheckbox(
        v_model=("directory_workflow", False),
        color="success",
        on_icon="mdi-folder-eye",
        off_icon="mdi-folder-eye",
        classes="mx-1",
        hide_details=True,
        dense=True,
    )
    vuetify.VCheckbox(
        v_model=("browse_workflow", False),
        color="success",
        on_icon="mdi-application",
        off_icon="mdi-application",
        classes="mx-1",
        hide_details=True,
        dense=True,
    )
    vuetify.VCheckbox(
        v_model=("scattering_workflow", False),
        color="success",
        on_icon="mdi-scatter-plot",
        off_icon="mdi-scatter-plot",
        classes="mx-1",
        hide_details=True,
        dense=True,
    )
    vuetify.VCheckbox(
        v_model=("transmission_workflow", False),
        color="success",
        on_icon="mdi-transfer",
        off_icon="mdi-transfer",
        classes="mx-1",
        hide_details=True,
        dense=True,
    )
    vuetify.VCheckbox(
        v_model=("image_workflow", False),
        color="success",
        on_icon="mdi-image-multiple",
        off_icon="mdi-image-multiple",
        classes="mx-1",
        hide_details=True,
        dense=True,
    )
