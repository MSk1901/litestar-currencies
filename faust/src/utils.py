def get_current_minute_interval(event_time: float, factor: int = 1) -> int:
    return int(event_time - (event_time % (60 * factor)))
