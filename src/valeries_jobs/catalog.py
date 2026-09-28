"""Career-to-skill data used by the first playable interview slice."""


SKILLS = {
    "acting": 194727,
    "apothecary": 439222,
    "charisma": 16699,
    "comedy": 16698,
    "cooking": 16705,
    "entrepreneur": 274197,
    "fabrication": 231908,
    "fishing": 39397,
    "fitness": 16659,
    "flower_arranging": 186703,
    "gardening": 16700,
    "handiness": 16704,
    "logic": 16706,
    "mischief": 16707,
    "mixology": 16695,
    "natural_living": 434909,
    "painting": 16708,
    "parenting": 160504,
    "photography": 105774,
    "programming": 16703,
    "research_debate": 221014,
    "robotics": 217413,
    "rocket_science": 16710,
    "romance": 368684,
    "thanatology": 380495,
    "video_gaming": 16712,
    "writing": 16714,
}


def _profile(name, primary, secondary=(), part_time=False):
    return {
        "name": name,
        "primary": primary,
        "secondary": tuple(secondary),
        "part_time": bool(part_time),
    }


CAREERS = {
    189135: _profile("Actor", "acting", ("charisma", "comedy")),
    107230: _profile("Doctor", "logic", ("charisma",)),
    107255: _profile("Scientist", "logic", ("handiness",)),
    135201: _profile("Politician", "charisma", ("logic",)),
    12893: _profile("Astronaut", "logic", ("fitness", "rocket_science")),
    106458: _profile("Athlete", "fitness", ("charisma",)),
    106460: _profile("Business", "charisma", ("logic",)),
    232767: _profile("Civil Designer", "logic", ("handiness", "fabrication")),
    204960: _profile("Conservationist", "logic", ("gardening", "charisma")),
    248315: _profile("Salaryperson", "logic", ("programming", "charisma")),
    27927: _profile("Criminal", "mischief", ("fitness", "charisma")),
    136115: _profile("Critic", "writing", ("charisma", "cooking")),
    9231: _profile("Culinary", "cooking", ("mixology", "charisma")),
    106132: _profile("Detective", "logic", ("fitness", "charisma")),
    219591: _profile("Education", "research_debate", ("logic", "charisma")),
    217872: _profile("Engineer", "robotics", ("programming", "handiness")),
    27929: _profile("Entertainer", "charisma", ("comedy",)),
    186159: _profile("Gardener", "gardening", ("flower_arranging",)),
    223298: _profile("Law", "research_debate", ("logic", "charisma")),
    202483: _profile("Military", "fitness", ("logic", "charisma")),
    439108: _profile("Naturopath", "natural_living", ("apothecary", "gardening")),
    27930: _profile("Painter", "painting", ("charisma",)),
    27931: _profile("Secret Agent", "logic", ("fitness", "charisma")),
    135363: _profile("Social Media", "charisma", ("writing", "comedy")),
    193202: _profile("Style Influencer", "charisma", ("painting", "writing")),
    27932: _profile("Tech Guru", "programming", ("video_gaming", "logic")),
    27933: _profile("Writer", "writing", ("charisma",)),
    377623: _profile("Reaper", "thanatology", ("fitness", "charisma")),
    377586: _profile("Mortician", "thanatology", ("fitness", "charisma")),
    366724: _profile("Romance Consultant", "romance", ("charisma", "writing")),
    208723: _profile("Babysitter", "charisma", ("parenting",), True),
    35221: _profile("Babysitter", "charisma", ("parenting",), True),
    208737: _profile("Barista", "mixology", ("charisma",), True),
    35220: _profile("Barista", "mixology", ("charisma",), True),
    208405: _profile("Diver", "fitness", ("logic",), True),
    208761: _profile("Fast Food Employee", "cooking", ("charisma",), True),
    35157: _profile("Fast Food Employee", "cooking", ("charisma",), True),
    207607: _profile("Fisherman", "fishing", ("fitness",), True),
    205662: _profile("Lifeguard", "fitness", ("charisma",), True),
    208881: _profile("Lifeguard", "fitness", ("charisma",), True),
    208779: _profile("Manual Laborer", "fitness", ("handiness", "gardening"), True),
    35218: _profile("Manual Laborer", "fitness", ("handiness", "gardening"), True),
    208874: _profile("Retail Employee", "charisma", ("logic",), True),
    35219: _profile("Retail Employee", "charisma", ("logic",), True),
    277662: _profile("Simfluencer", "entrepreneur", ("charisma", "photography"), True),
    277663: _profile("Simfluencer", "entrepreneur", ("charisma", "photography"), True),
    273912: _profile("Video Game Streamer", "video_gaming", ("entrepreneur", "charisma"), True),
    273911: _profile("Video Game Streamer", "video_gaming", ("entrepreneur", "charisma"), True),
    353302: _profile("Handyperson", "handiness", ("fitness",), True),
}


DEFERRED_CAREER_IDS = {257934}


def get_profile(career_type):
    return CAREERS.get(int(career_type.guid64))


def should_bypass(career_type):
    """Fail open for Noble, gig systems, and careers not mapped yet."""

    name = getattr(career_type, "__name__", "").lower()
    career_id = int(getattr(career_type, "guid64", 0))
    return "noble" in name or career_id in DEFERRED_CAREER_IDS or career_id not in CAREERS
