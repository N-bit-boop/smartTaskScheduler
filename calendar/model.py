from dataclasses import dataclass
from timecore.time_rep import TimePoint
from timecore.intervals import TimeInterval


@dataclass(frozen=True)
class CalendarEvent:
    start: TimePoint
    end:  TimePoint
    description: str | None = None #An optional 
    source : str | None = None #An optional

    def __post_init__(self):
        if self.start >= self.end:
            raise ValueError("Strat needs to be before the end")
    

    def to_interval(self) -> TimeInterval:
        return TimeInterval(self.start, self.end)