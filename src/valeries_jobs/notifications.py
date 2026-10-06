"""Small wrappers around native Sims 4 modal dialogs."""

from ui.ui_dialog import UiDialogOk
from valeries_jobs.localization import text


def show_dialog(title, body, sim_info=None):
    dialog = UiDialogOk.TunableFactory().default(
        sim_info,
        title=lambda *args, **kwargs: title,
        text=lambda *args, **kwargs: body,
        text_ok=lambda *args, **kwargs: text("dialog.ok"),
    )
    dialog.show_dialog()
