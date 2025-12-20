from dataclasses import dataclass
from typing import Iterable, List
from timecore.time_rep import TimePoint
from timecore.intervals import TimeInterval
from datetime import timedelta


@dataclass(frozen=True)

class Routine:
    name: str 
    duration: int 
    recurrence: int
    start_time: TimePoint
    flexible_minutes: int 
    protected:bool = True 

    #Determines if the routine is on a sepcific , reccurence will be the bit mask of the weekday
    def expands_on(self, weekday:int ) ->bool:
        return (self.recurrence >> weekday) & 1 == 1
    
    def expand(self, window: TimeInterval) -> List[TimeInterval]:
        intervals: List[TimeInterval]= []

        current_date = window.start.date
        end_date = window.end.date 


        while current_date <= end_date:
            weekday = current_date.weekday()

            if self.expands_on(weekday):
                start = TimePoint.combine(current_date, self.start_time)
                end = start.add_minutes(self.duration)

                candidate = TimeInterval(start, end)

                if candidate.overlaps(window):
                    clipped_start = max(candidate.start, window.start)
                    clipped_end = min(candidate.end, window.end)
                    intervals.append(TimeInterval(clipped_start, clipped_end))
        
        current_date +=timedelta(days=1)

        return intervals