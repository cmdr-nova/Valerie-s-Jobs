"""Development commands for verifying that the script loads in game."""

import sims4.commands
import sims4.log

from valeries_jobs.scoring import calculate_interview_chance, resolve_interview
from valeries_jobs.version import MOD_NAME, MOD_VERSION


LOGGER = sims4.log.Logger("ValeriesJobs", default_owner="Valerie")


@sims4.commands.Command("vj.hello", command_type=sims4.commands.CommandType.Live)
def valeries_jobs_hello(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    message = "{} {} initialized.".format(MOD_NAME, MOD_VERSION)
    output(message)
    LOGGER.info(message)


@sims4.commands.Command("vj.test_apply", command_type=sims4.commands.CommandType.Live)
def valeries_jobs_test_apply(charisma: int = 0, primary_skill: int = 0, _connection=None):
    output = sims4.commands.CheatOutput(_connection)
    chance = calculate_interview_chance(
        primary_level=primary_skill,
        charisma_level=charisma,
    )
    result = resolve_interview(chance)
    message = (
        "Valerie's Jobs test interview: {chance}% chance, rolled {roll}: {outcome}."
    ).format(**result)
    output(message)
    LOGGER.info(message)


@sims4.commands.Command("vj.complete_interview", command_type=sims4.commands.CommandType.Live)
def valeries_jobs_complete_interview(_connection=None):
    """Finish the active Sim's pending interview during development testing."""

    import services
    from valeries_jobs.interviews import complete_interview_for_test, _PENDING

    output = sims4.commands.CheatOutput(_connection)
    client = services.client_manager().get(_connection)
    sim_info = client.active_sim_info if client is not None else None
    if sim_info is None or sim_info.id not in _PENDING:
        output("Valerie's Jobs: the active Sim has no pending interview.")
        return
    complete_interview_for_test(sim_info.id)
    output("Valerie's Jobs: pending interview completed for testing.")
