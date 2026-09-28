"""Small wrappers around native Sims 4 modal dialogs."""

from sims4.localization import LocalizationHelperTuning
from ui.ui_dialog import UiDialogOk


def show_dialog(title, body, sim_info=None):
    dialog = UiDialogOk.TunableFactory().default(
        sim_info,
        title=lambda *args, **kwargs: LocalizationHelperTuning.get_raw_text(title),
        text=lambda *args, **kwargs: LocalizationHelperTuning.get_raw_text(body),
        text_ok=lambda *args, **kwargs: LocalizationHelperTuning.get_raw_text("OK"),
    )
    dialog.show_dialog()
