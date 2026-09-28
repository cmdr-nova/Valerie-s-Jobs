"""Career interception and timed interview resolution."""

import random

import alarms
import clock
import sims4.log
from careers.career_tracker import CareerTracker

from valeries_jobs.catalog import get_profile, should_bypass
from valeries_jobs.game_skills import read_profile_levels
from valeries_jobs.notifications import show_dialog
from valeries_jobs.rabbit_holes import (
    finish_interview_rabbit_hole,
    start_interview_rabbit_hole,
)
from valeries_jobs.scoring import calculate_interview_chance, resolve_interview


LOGGER = sims4.log.Logger("ValeriesJobs", default_owner="Valerie")
GHOST_LISTING_CHANCE = 0.08
_PENDING = {}
_ORIGINAL_ADD_CAREER = CareerTracker.add_career


def _sim_name(sim_info):
    return getattr(sim_info, "first_name", "Your Sim")


def _feedback(profile, levels, result):
    if result["outcome"] == "ghosted":
        return (
            "The employer decided not to fill the position after all. "
            "This was a ghost listing, so the interview was never winnable."
        )
    primary_name = profile["primary"].replace("_", " ").title()
    primary_level = levels["primary"]
    if result["outcome"] == "accepted":
        if primary_level >= 2:
            reason = "Their {} skill made a strong entry-level impression.".format(primary_name)
        else:
            reason = "Their potential and interview answers won the employer over."
        return "The offer is official! {}".format(reason)
    if primary_level < 2:
        reason = "Building {} to level 2 or 3 would make the next application stronger.".format(primary_name)
    elif levels["charisma"] < 2:
        reason = "The qualifications were promising, but the interview answers did not quite land."
    else:
        reason = "They interviewed well, but another applicant narrowly edged them out."
    return "No offer this time. {}".format(reason)


def _complete_interview(sim_id):
    application = _PENDING.pop(sim_id, None)
    if application is None:
        return
    sim_info = application["sim_info"]
    career = application["career"]
    profile = application["profile"]
    levels = read_profile_levels(sim_info, profile)
    chance = calculate_interview_chance(
        primary_level=levels["primary"],
        secondary_levels=levels["secondary"],
        charisma_level=levels["charisma"],
        base_chance=50 if profile["part_time"] else 40,
    )
    ghost_listing = random.random() < GHOST_LISTING_CHANCE
    result = resolve_interview(chance, ghost_listing=ghost_listing)
    career_name = profile["name"]
    feedback = _feedback(profile, levels, result)

    if result["outcome"] == "accepted":
        if sim_info.career_tracker.get_career_by_uid(career.guid64) is None:
            kwargs = dict(application["kwargs"])
            kwargs["show_confirmation_dialog"] = False
            _ORIGINAL_ADD_CAREER(sim_info.career_tracker, career, **kwargs)
        title = "{} Interview: You're Hired!".format(career_name)
    elif result["outcome"] == "ghosted":
        title = "{} Interview: Position Withdrawn".format(career_name)
    else:
        title = "{} Interview: No Offer".format(career_name)

    if result["outcome"] == "ghosted":
        body = feedback
    else:
        body = "{}\n\nInterview chance: {}%.".format(feedback, result["chance"])
    show_dialog(title, body, sim_info)
    LOGGER.info(
        "Interview completed for {}: career={}, chance={}, roll={}, outcome={}",
        sim_info,
        career_name,
        result["chance"],
        result["roll"],
        result["outcome"],
    )


def _start_interview(tracker, new_career, kwargs):
    sim_info = tracker._sim_info
    sim_id = sim_info.id
    if sim_id in _PENDING:
        show_dialog(
            "Interview Already Scheduled",
            "{} is already completing a job interview.".format(_sim_name(sim_info)),
            sim_info,
        )
        return

    profile = get_profile(type(new_career))
    duration = random.choice((1, 2))
    application = {
        "sim_info": sim_info,
        "career": new_career,
        "profile": profile,
        "kwargs": kwargs,
        "duration": duration,
    }
    _PENDING[sim_id] = application

    def _finish_safely():
        try:
            _complete_interview(sim_id)
        except Exception as error:
            _PENDING.pop(sim_id, None)
            LOGGER.error("Interview completion failed: {}", error)

    def _on_rabbit_hole_exit(canceled=False):
        if canceled:
            _PENDING.pop(sim_id, None)
            show_dialog(
                "{} Interview Canceled".format(profile["name"]),
                "{} left the interview before it was completed. The application was withdrawn.".format(
                    _sim_name(sim_info)
                ),
                sim_info,
            )
            return
        _finish_safely()

    def _on_rabbit_hole_enter():
        show_dialog(
            "{} Interview Started".format(profile["name"]),
            "{} has arrived for the interview. It will take {} in-game hour{}. "
            "Relevant skills are being considered now.".format(
                _sim_name(sim_info), duration, "" if duration == 1 else "s"
            ),
            sim_info,
        )

    application["rabbit_hole_id"] = start_interview_rabbit_hole(
        sim_info,
        duration,
        _on_rabbit_hole_enter,
        _on_rabbit_hole_exit,
    )
    if application["rabbit_hole_id"] is None:
        def _on_alarm(_alarm_handle):
            _finish_safely()

        application["alarm"] = alarms.add_alarm(
            sim_info,
            clock.interval_in_sim_hours(duration),
            _on_alarm,
            cross_zone=True,
        )
        LOGGER.warn("Interview rabbit hole unavailable; using timed fallback for {}", sim_info)
        _on_rabbit_hole_enter()
    LOGGER.info("Started {} hour interview for {} ({})", duration, sim_info, profile["name"])


def _intercepted_add_career(self, new_career, *args, **kwargs):
    show_confirmation = kwargs.get("show_confirmation_dialog", False)
    career_type = type(new_career)
    sim_info = getattr(self, "_sim_info", None)
    if (
        not show_confirmation
        or sim_info is None
        or not getattr(sim_info, "is_selectable", False)
        or should_bypass(career_type)
    ):
        return _ORIGINAL_ADD_CAREER(self, new_career, *args, **kwargs)

    captured = dict(kwargs)
    captured.pop("show_confirmation_dialog", None)
    _start_interview(self, new_career, captured)


def install_interview_hook():
    if CareerTracker.add_career is not _intercepted_add_career:
        CareerTracker.add_career = _intercepted_add_career
        LOGGER.info("Valerie's Jobs career interview hook installed.")


def complete_interview_for_test(sim_id):
    application = _PENDING.get(sim_id)
    if application is None:
        return False
    rabbit_hole_id = application.get("rabbit_hole_id")
    if rabbit_hole_id is not None:
        if finish_interview_rabbit_hole(sim_id, rabbit_hole_id):
            return True
    _complete_interview(sim_id)
    return True
