"""Interaction class that hides a Sim after routing to the lot exit marker."""

from interactions.base.super_interaction import SuperInteraction
from interactions.interaction_finisher import FinishingType
from interactions.priority import Priority
from interactions.rabbit_hole import HIDE_SIM_LIABILTIY, HideSimLiability
from interactions.utils.tunable import CriticalPriorityLiability

from valeries_jobs.arrival_callbacks import notify_interview_arrival


AUTONOMY_REPLACEMENT_FINISHING_TYPES = frozenset((
    FinishingType.AUTO_EXIT,
    FinishingType.DISPLACED,
    FinishingType.INTERACTION_INCOMPATIBILITY,
    FinishingType.INTERACTION_QUEUE,
    FinishingType.PRIORITY,
    FinishingType.SOCIALS,
))


class JobInterviewInteraction(SuperInteraction):
    """A routed off-screen interaction without tuning-defined liabilities."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        critical_token = CriticalPriorityLiability.LIABILITY_TOKEN
        if self.get_liability(critical_token) is None:
            self.add_liability(
                critical_token,
                CriticalPriorityLiability(
                    self,
                    priority_on_run=Priority.Critical,
                    priority_on_push=Priority.Critical,
                ),
            )
        if self.get_liability(HIDE_SIM_LIABILTIY) is None:
            self.add_liability(HIDE_SIM_LIABILTIY, HideSimLiability(self))

    def _run_interaction_gen(self, timeline):
        """Announce the interview only after routing to the lot exit succeeds."""
        notify_interview_arrival(self.sim.id)
        return (yield from super()._run_interaction_gen(timeline))

    def displace(self, displaced_by, *args, **kwargs):
        """Keep autonomous actions from replacing an active interview."""
        return False

    def _cancel_eventually(self, *args, **kwargs):
        """Ignore queue replacement while retaining genuine exit paths."""
        finishing_type = args[0] if args else kwargs.get("finishing_type")
        if finishing_type in AUTONOMY_REPLACEMENT_FINISHING_TYPES:
            return False
        return super()._cancel_eventually(*args, **kwargs)
