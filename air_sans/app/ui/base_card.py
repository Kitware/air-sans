from trame.widgets import html, vuetify

# -----------------------------------------------------------------------------
# Base Card Components
# -----------------------------------------------------------------------------


def ui_card_title(title, ui_icon):
    with vuetify.VCardTitle(
        classes="grey lighten-1 pa-0 grey--text text--darken-3",
        style="user-select: none; cursor: pointer",
        hide_details=True,
        dense=True,
    ) as card_title:
        vuetify.VIcon(ui_icon, classes="mr-3", color="grey darken-3")
        html.Div(title)
    return card_title


def ui_card_text():
    card_text = vuetify.VCardText(classes="pa-1")
    return card_text


def ui_card_actions():
    card_actions = vuetify.VCardActions(
        classes="px-0 py-1",
        hide_details=True,
        dense=True,
    )
    return card_actions


def ui_card(ui_name):
    card = vuetify.VCard(
        classes="ma-1 rounded elevation-8",
        v_show=ui_name,
    )
    return card
