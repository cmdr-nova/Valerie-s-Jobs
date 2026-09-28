"""Interaction class that hides a Sim after routing to the lot exit marker."""

from interactions.base.super_interaction import SuperInteraction
from interactions.rabbit_hole import HIDE_SIM_LIABILTIY, HideSimLiability


class JobInterviewInteraction(SuperInteraction):
    """A routed off-screen interaction without tuning-defined liabilities."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.get_liability(HIDE_SIM_LIABILTIY) is None:
            self.add_liability(HIDE_SIM_LIABILTIY, HideSimLiability(self))
