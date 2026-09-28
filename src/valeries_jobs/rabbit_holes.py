"""Native managed rabbit-hole bridge for off-screen job interviews."""

import services
import sims4.resources


RABBIT_HOLE_IDS = {
    1: 5556844565946566721,
    2: 10092612624710672942,
}


def start_interview_rabbit_hole(sim_info, duration_hours, on_exit):
    manager = services.get_instance_manager(sims4.resources.Types.RABBIT_HOLE)
    rabbit_hole_type = manager.get(RABBIT_HOLE_IDS[int(duration_hours)])
    service = services.get_rabbit_hole_service()
    if rabbit_hole_type is None or service is None:
        return None
    if service.is_in_rabbit_hole(sim_info.id):
        return None

    rabbit_hole_id = service.put_sim_in_managed_rabbithole(
        sim_info,
        rabbit_hole_type=rabbit_hole_type,
    )
    if rabbit_hole_id is None:
        return None
    service.set_rabbit_hole_expiration_callback(
        sim_info.id,
        rabbit_hole_id,
        on_exit,
    )
    return rabbit_hole_id


def finish_interview_rabbit_hole(sim_id, rabbit_hole_id):
    service = services.get_rabbit_hole_service()
    if service is None or not service.is_in_rabbit_hole(sim_id, rabbit_hole_id):
        return False
    service.remove_sim_from_rabbit_hole(sim_id, rabbit_hole_id, canceled=False)
    return True
