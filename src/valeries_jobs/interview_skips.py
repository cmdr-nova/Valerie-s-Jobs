"""Session-only, per-Sim interview skips; no game imports required."""


class InterviewSkips:
    def __init__(self):
        # None means armed; a career UID means EA's confirmation may be pending.
        self._armed = {}

    def arm(self, sim_id):
        self._armed.setdefault(sim_id, None)

    def cancel(self, sim_id):
        if sim_id not in self._armed:
            return False
        del self._armed[sim_id]
        return True

    def should_skip(self, sim_id, career_uid, is_application):
        return sim_id in self._armed and (
            is_application or self._armed[sim_id] == career_uid
        )

    def join(self, tracker, career, add_career, *args, **kwargs):
        sim_id = tracker._sim_info.id
        career_uid = career.guid64
        already_joined = tracker.get_career_by_uid(career_uid) is not None
        self._armed[sim_id] = career_uid
        # Preserve EA's confirmations, shift/agency selections, args and result.
        # A confirmation can call add_career again later with show_confirmation=False.
        result = add_career(tracker, career, *args, **kwargs)
        if not already_joined and tracker.get_career_by_uid(career_uid) is not None:
            self.cancel(sim_id)
        return result


INTERVIEW_SKIPS = InterviewSkips()
