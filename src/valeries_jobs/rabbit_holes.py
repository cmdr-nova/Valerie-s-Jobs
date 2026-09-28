"""Native managed rabbit-hole bridge for off-screen job interviews."""

import services
import sims4.resources

from valeries_jobs.arrival_callbacks import (
    discard_arrival_callback,
    register_arrival_callback,
)


RABBIT_HOLE_IDS = {
    1: 5556844565946566721,
    2: 10092612624710672942,
}


def start_interview_rabbit_hole(sim_info, duration_hours, on_enter, on_exit):
    manager = services.get_instance_manager(sims4.resources.Types.RABBIT_HOLE)
    rabbit_hole_type = manager.get(RABBIT_HOLE_IDS[int(duration_hours)])
    service = services.get_rabbit_hole_service()
    if rabbit_hole_type is None or service is None:
        return None
    if service.is_in_rabbit_hole(sim_info.id):
        return None

    register_arrival_callback(sim_info.id, on_enter)
    try:
        rabbit_hole_id = service.put_sim_in_managed_rabbithole(
            sim_info,
            rabbit_hole_type=rabbit_hole_type,
        )
    except Exception:
        discard_arrival_callback(sim_info.id)
        raise
    if rabbit_hole_id is None:
        discard_arrival_callback(sim_info.id)
        return None

    def _on_exit(*args, **kwargs):
        discard_arrival_callback(sim_info.id)
        return on_exit(*args, **kwargs)

    service.set_rabbit_hole_expiration_callback(
        sim_info.id,
        rabbit_hole_id,
        _on_exit,
    )
    return rabbit_hole_id


def finish_interview_rabbit_hole(sim_id, rabbit_hole_id):
    service = services.get_rabbit_hole_service()
    if service is None or not service.is_in_rabbit_hole(sim_id, rabbit_hole_id):
        return False
    discard_arrival_callback(sim_id)
    service.remove_sim_from_rabbit_hole(sim_id, rabbit_hole_id, canceled=False)
    return True
