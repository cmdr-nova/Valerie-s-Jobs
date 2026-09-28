"""Pure interview scoring logic, kept independent of The Sims 4 runtime."""

import random


def _clamp(value, minimum, maximum):
    return max(minimum, min(maximum, value))


def _skill_bonus(level, maximum_bonus):
    normalized_level = _clamp(int(level), 0, 10)
    return round((normalized_level / 10.0) * maximum_bonus)


def calculate_interview_chance(
    primary_level=0,
    secondary_levels=(),
    charisma_level=0,
    base_chance=30,
    degree_bonus=0,
    mood_modifier=0,
    trait_modifier=0,
    minimum=5,
    maximum=95,
):
    """Return a bounded, integer acceptance percentage."""

    primary_bonus = _skill_bonus(primary_level, 25)
    secondary_values = tuple(secondary_levels)[:3]
    secondary_bonus = sum(_skill_bonus(level, 5) for level in secondary_values)
    charisma_bonus = _skill_bonus(charisma_level, 10)

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

