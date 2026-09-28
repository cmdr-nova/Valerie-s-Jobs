"""Safe bridge between the domain scorer and EA's statistic tracker."""

import services
import sims4.resources

from valeries_jobs.catalog import SKILLS


def get_skill_level(sim_info, skill_name):
    skill_id = SKILLS.get(skill_name)
    if skill_id is None:
        return 0
    manager = services.get_instance_manager(sims4.resources.Types.STATISTIC)
    skill_type = manager.get(skill_id)
    if skill_type is None:
        return 0
    skill = sim_info.get_statistic(skill_type, add=False)
    if skill is None:
        return 0
    try:
        if sim_info.is_instanced():
            return int(sim_info.get_effective_skill_level(skill))
    except Exception:
        pass
    try:
        return int(skill.get_user_value())
    except Exception:
        return 0


def read_profile_levels(sim_info, profile):
    return {
        "primary": get_skill_level(sim_info, profile["primary"]),
        "secondary": tuple(
            get_skill_level(sim_info, skill_name)
            for skill_name in profile["secondary"]
            if skill_name != "charisma"
        ),
        "charisma": get_skill_level(sim_info, "charisma"),
    }
