import json
from pathlib import Path
from typing import List, Optional

from domain.routines import Routine
from timecore.time_rep import TimePoint

ROUTINE_PATH = Path("data/routines.json")
ROUTINE_PATH.parent.mkdir(parents=True, exist_ok=True)


WEEKDAY_MAP ={
    "mon" : 0,
    "tue" : 1,
    "wed" : 2,
    "thur" : 3,
    "fri" : 4,
    "sat" : 5,
    "sun" : 6,
}


def _weekdays_to_mask(days: List[str]) -> int:
    mask = 0
    for d in days:
        d= d.lower()
        if d not in WEEKDAY_MAP:
            raise ValueError(f"Invalid weekday: {d}")
        mask |= 1 << WEEKDAY_MAP[d]
    return mask

def _mask_to_weekdays(mask: int) -> List[str]:
    result  = []
    for d, i in WEEKDAY_MAP.items():
        if mask & (1<<i):
            result.append(d)
    return result

def _routine_to_dict(r: Routine) -> dict:
     return {
        "name": r.name,
        "start_time": f"{r.start_time.minute() // 60:02d}:{r.start_time.minute() % 60:02d}",
        "duration": r.duration,
        "weekdays": _mask_to_weekdays(r.weekdays),
        "protected": r.protected,
    }

def _dict_to_routine(data: dict) -> Routine:
    try:
        name = data["name"]
        start_raw = data["start_time"]
        duration = data["duration"]
        weekdays_raw = data["weekdays"]
        protected = data["protected"]
    except KeyError as e:
        raise ValueError(f"Missing field: {e}")

    # Name
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Routine name must be a non-empty string")

    # Start time
    try:
        h, m = map(int, start_raw.split(":"))
        start_time = TimePoint(h * 60 + m)
    except Exception:
        raise ValueError(f"Invalid start_time format: {start_raw}")

    # Duration
    if not isinstance(duration, int) or duration <= 0:
        raise ValueError("Routine duration must be a positive integer")

    if start_time.minute() + duration > 1440:
        raise ValueError("Routine exceeds day boundary")

    # Weekdays
    if not isinstance(weekdays_raw, list) or not weekdays_raw:
        raise ValueError("Weekdays must be a non-empty list")

    weekdays = _weekdays_to_mask(weekdays_raw)

    # Protected
    if not isinstance(protected, bool):
        raise ValueError("Protected must be boolean")

    return Routine(
        name=name,
        start_time=start_time,
        duration=duration,
        weekdays=weekdays,
        protected=protected,
    )


def load_routines() ->List[Routine]:
    if not ROUTINE_PATH.exists():
        return []
    
    try:
        with ROUTINE_PATH.open("r", encoding="utf-8") as f:
            raw = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError("Malformed routines.json") from e 
    
    if not isinstance(raw,list):
        raise ValueError(".json must conatina a list")
    
    routines: List[Routine] = []
    seen =set()

    for entry in raw:
        r = _dict_to_routine(entry)

        if r.name in seen:
            raise ValueError(f"duplciate routine name {r.name}")
        seen.add(r.name)

        routines.append(r)

    return routines

def save_routines(routines: List[Routine]) -> None:
    data =[_routine_to_dict(r) for r in routines]
    with ROUTINE_PATH.open("w", encoding="utf-8") as f:
        json.dump(data,f, indent =2)

def add_routine(routine: Routine) -> None:
    routines = load_routines()

    if any(r.name == routine.name for r in routines):
        raise ValueError(f"boi i caught a duplicate {routine.name}")
    
    routines.append(routine)
    save_routines(routines)


def remove_routine(name: str) -> bool:
    routines = load_routines()

    new = [ r for r in routines if r.name != name]

    if len(new) == len(routines):
        return False 
    
    save_routines(new)
    return True


