from domain.routines import Routine
from typing import List
from timecore.intervals import TimeInterval

def routine_adapter(window: TimeInterval, routines: List[Routine], weekday: int) -> List[TimeInterval]:
    blocked: List[TimeInterval] = [] #Type hint and empty list

    for r in routines:
        interval =  r.expand_for_day(window, weekday)

        if interval is not None:
            blocked.append(interval)

    return blocked 
