from dataclasses import dataclass
from typing import Iterable, List
from timecore.time_rep import TimePoint
from timecore.intervals import TimeInterval


@dataclass(frozen=True)

class Routine:
    name: str 
    duration: int 
    recurrence: int
    start_time: TimePoint
    flexible_minutes: int 
    protected:bool = True 