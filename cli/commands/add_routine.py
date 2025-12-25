from domain.routines import Routine
from timecore.time_rep import TimePoint
from cli.storage.routines_store import add_routine

WEEKDAY_MAP ={
    "mon" : 0,
    "tue" : 1,
    "wed" : 2,
    "thur" : 3,
    "fri" : 4,
    "sat" : 5,
    "sun" : 6,
}


def prompt (msg :str) -> str:
    return input(msg).strip()

def parse_start_time(raw: str):
    if not raw:
        return None

    try:
        parts = raw.split(":")
        if len(parts) != 2:
            raise ValueError

        h, m = map(int, parts)
        if not (0 <= h < 24 and 0 <= m < 60):
            raise ValueError

        return TimePoint(h * 60 + m)

    except Exception:
        raise ValueError("Deadline must be in HH:MM (24-hour) format")
    

def parse_recurrence(raw: str) -> int:
    if not raw:
        raise ValueError("Days cannot be empty")

    days = [d.strip().lower() for d in raw.split(",")]
    mask = 0

    for d in days:
        if d not in WEEKDAY_MAP:
            raise ValueError(f"Invalid weekday: {d}")
        mask |= 1 << WEEKDAY_MAP[d]

    return mask


def run():
    try:
        name = prompt("Routine name: ")

        start_raw = prompt("Start time (HH:MM): ")
        start_time = parse_start_time(start_raw)

        duration = int(prompt("Duration (minutes): "))
        if duration <= 0:
            raise ValueError("Duration must be positive")

        days_raw = prompt("Days (mon,tue,wed,thu,fri): ")
        recurrence = parse_recurrence(days_raw)

        protected_raw = prompt("Protected? (y/n): ").lower()
        protected = protected_raw == "y"

        routine = Routine(
            name=name,
            start_time=start_time,
            duration=duration,
            recurrence=recurrence,   
            protected=protected,
        )

        add_routine(routine)
        print(f"✔ Routine added: {name}")

    except Exception as e:
        print(f"✖ Error: {e}")