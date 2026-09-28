"""Temporary moodlets granted by interview outcomes."""

import services
import sims4.log
import sims4.resources


LOGGER = sims4.log.Logger("ValeriesJobs", default_owner="Valerie")

OUTCOME_BUFF_IDS = {
    "accepted": 8465629208866944119,
    "rejected": 15001183660286003602,
    "ghosted": 6217764197368866584,
}


def apply_outcome_moodlet(sim_info, outcome):
    """Apply the tuned moodlet for an interview outcome without blocking completion."""
    buff_id = OUTCOME_BUFF_IDS.get(outcome)
    if buff_id is None:
        return False
    buff_manager = services.get_instance_manager(sims4.resources.Types.BUFF)
    buff_type = buff_manager.get(buff_id)
    if buff_type is None:
        LOGGER.warn("Interview outcome buff {} was not loaded for {}", buff_id, outcome)
        return False
    try:
        sim_info.add_buff(buff_type)
    except Exception as error:
        LOGGER.error("Could not apply interview outcome buff {}: {}", outcome, error)
        return False
    return True
