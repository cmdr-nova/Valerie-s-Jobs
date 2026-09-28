"""One-shot callbacks fired when an interview interaction reaches its destination."""


_CALLBACKS = {}


def register_arrival_callback(sim_id, callback):
    _CALLBACKS[sim_id] = callback


def discard_arrival_callback(sim_id):
    _CALLBACKS.pop(sim_id, None)


def notify_interview_arrival(sim_id):
    callback = _CALLBACKS.pop(sim_id, None)
    if callback is None:
        return False
    callback()
    return True
