import json
from pathlib import Path
from typing import List

from domain.routines import Routine
from timecore.time_rep import TimePoint

ROUTINE_PATH = Path("data/routines.json")
ROUTINE_PATH.parent.mkdir(parents=True, exist_ok=True)



def _routine_to_dict(r: Routine) -> dict:
    return {
        "name": r.name,
        "start_time": f"{r.start_time.minute() // 60:02d}:{r.start_time.minute() % 60:02d}",
        "duration": r.duration,
        "recurrence": r.recurrence,   #  STORE BITMASK
        "protected": r.protected,
    }


def _dict_to_routine(data: dict) -> Routine:
    try:
        name = data["name"]
        start_raw = data["start_time"]
        duration = data["duration"]
        recurrence = data["recurrence"]
        protected = data["protected"]
    except KeyError as e:
        raise ValueError(f"Missing field: {e}")

    # name
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Routine name must be a non-empty string")

    # start time
    try:
        h, m = map(int, start_raw.split(":"))
        start_time = TimePoint(h * 60 + m)
    except Exception:
        raise ValueError(f"Invalid start_time format: {start_raw}")

    # duration
    if not isinstance(duration, int) or duration <= 0:
        raise ValueError("Routine duration must be positive")

    if start_time.minute() + duration > 1440:
        raise ValueError("Routine exceeds day boundary")

    # recurrence (bitmask)
    if not isinstance(recurrence, int) or recurrence <= 0:
        raise ValueError("Recurrence must be a positive integer bitmask")

    # protected
    if not isinstance(protected, bool):
        raise ValueError("Protected must be boolean")

    return Routine(
        name=name,
        start_time=start_time,
        duration=duration,
        recurrence=recurrence,
        protected=protected,
    )




def load_routines() -> List[Routine]:
    if not ROUTINE_PATH.exists():
        return []

    try:
        with ROUTINE_PATH.open("r", encoding="utf-8") as f:
            raw = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError("Malformed routines.json") from e

    if not isinstance(raw, list):
        raise ValueError("routines.json must contain a list")

    routines: List[Routine] = []
    seen = set()

    for entry in raw:
        r = _dict_to_routine(entry)

        if r.name in seen:
            raise ValueError(f"Duplicate routine name: {r.name}")

        seen.add(r.name)
        routines.append(r)

    return routines


def save_routines(routines: List[Routine]) -> None:
    data = [_routine_to_dict(r) for r in routines]
    with ROUTINE_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def add_routine(routine: Routine) -> None:
    routines = load_routines()

    if any(r.name == routine.name for r in routines):
        raise ValueError(f"Duplicate routine name: {routine.name}")

    routines.append(routine)
    save_routines(routines)


def remove_routine(name: str) -> bool:
    routines = load_routines()
    new = [r for r in routines if r.name != name]

    if len(new) == len(routines):
        return False

    save_routines(new)
    return True
