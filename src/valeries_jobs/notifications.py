"""Small, dependency-free wrappers around native Sims 4 notifications."""

from sims4.localization import LocalizationHelperTuning
from ui.ui_dialog_notification import UiDialogNotification


def show_notification(title, body):
    dialog = UiDialogNotification.TunableFactory().default(
        None,
        title=lambda *args, **kwargs: LocalizationHelperTuning.get_raw_text(title),
        text=lambda *args, **kwargs: LocalizationHelperTuning.get_raw_text(body),
    )
    dialog.show_dialog()
