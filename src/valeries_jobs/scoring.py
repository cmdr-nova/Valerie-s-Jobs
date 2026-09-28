"""Pure interview scoring logic, kept independent of The Sims 4 runtime."""

import random


def _clamp(value, minimum, maximum):
    return max(minimum, min(maximum, value))


def _entry_skill_bonus(level, level_two_bonus, level_three_bonus, maximum_bonus):
    """Reward beginner skill levels strongly, then taper later gains."""

    normalized_level = _clamp(int(level), 0, 10)
    if normalized_level == 0:
        return 0
    if normalized_level == 1:
        return level_two_bonus // 2
    if normalized_level == 2:
        return level_two_bonus
    if normalized_level == 3:
        return level_three_bonus
    remaining_levels = 10 - 3
    remaining_bonus = maximum_bonus - level_three_bonus
    return level_three_bonus + round(
        ((normalized_level - 3) / float(remaining_levels)) * remaining_bonus
    )


def calculate_interview_chance(
    primary_level=0,
    secondary_levels=(),
    charisma_level=0,
    base_chance=40,
    degree_bonus=0,
    mood_modifier=0,
    trait_modifier=0,
    minimum=5,
    maximum=95,
):
    """Return a bounded, integer acceptance percentage."""

    primary_bonus = _entry_skill_bonus(primary_level, 16, 24, 35)
    secondary_values = tuple(secondary_levels)[:3]
    secondary_bonus = sum(
        _entry_skill_bonus(level, 3, 5, 8) for level in secondary_values
    )
    charisma_bonus = _entry_skill_bonus(charisma_level, 6, 9, 15)

    raw_chance = (
        int(base_chance)
        + primary_bonus
        + secondary_bonus
        + charisma_bonus
        + int(degree_bonus)
        + int(mood_modifier)
        + int(trait_modifier)
    )
    return int(_clamp(raw_chance, minimum, maximum))


def resolve_interview(chance, ghost_listing=False, rng=None):
    """Resolve an interview and return transparent diagnostic data."""

    bounded_chance = int(_clamp(int(chance), 0, 100))
    generator = rng if rng is not None else random
    roll = generator.randint(1, 100)

    if ghost_listing:
        outcome = "ghosted"
    elif roll <= bounded_chance:
        outcome = "accepted"
    else:
        outcome = "rejected"

    return {
        "chance": bounded_chance,
        "roll": roll,
        "outcome": outcome,
        "ghost_listing": bool(ghost_listing),
    }
