"""Valerie's Jobs script entry point."""

try:
    import sims4  # noqa: F401
except ImportError:
    # Pure domain modules are also tested outside the game runtime.
    pass
else:
    from valeries_jobs.interviews import install_interview_hook

    install_interview_hook()
    from valeries_jobs.commands import *  # noqa: F401,F403
