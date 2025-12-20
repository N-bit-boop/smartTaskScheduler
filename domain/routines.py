from dataclasses import dataclass
from typing import Optional
from timecore.time_rep import TimePoint
from timecore.intervals import TimeInterval

@dataclass(frozen=True)
class Routine:
    name: str
    start_time: TimePoint          # time of day
    duration: int                  # minutes
    recurrence: int                # weekday bitmask (0 = Mon … 6 = Sun)
    flexible_minutes: int = 0
    protected: bool = True

    def expands_on(self, weekday: int) -> bool:
        #if it applies to a day of the week with a routine 
        return (self.recurrence >> weekday) & 1 == 1

    def expand_for_day(self, window: TimeInterval, weekday: int) -> Optional[TimeInterval]:
        
        #Expand this routine into a TimeInterval for a single day.
        #Returns None if the routine does not apply or does not overlap.
        

        # Does not run on this day
        if not self.expands_on(weekday):
            return None

        # Build routine interval
        try:
            start = self.start_time
            end = start.add_minutes(self.duration)
        except ValueError:
            # Routine crosses midnight → not supported in base system
            return None

        candidate = TimeInterval(start, end)

        # No overlap with planning window
        if not candidate.overlaps(window):
            return None

        # Clip to planning window
        clipped_start = max(candidate.start, window.start)
        clipped_end = min(candidate.end, window.end)

        return TimeInterval(clipped_start, clipped_end)
