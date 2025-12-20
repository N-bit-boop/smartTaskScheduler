from dataclasses import dataclass
from functools import total_ordering

@total_ordering
@dataclass(frozen=True)
class TimePoint:
    _minute: int #minutes since midnite 

    def __post_init__(self):
        if not (0 <= self._minute < 1440):
            raise ValueError("TimePoint must be within a single day")

    def minute(self) -> int:
        return self._minute

    def __str__(self):
        h = self._minute // 60
        m = self._minute % 60
        return f"{h:02d}:{m:02d}"

    def __lt__(self, other: "TimePoint") -> bool:
        if not isinstance(other, TimePoint):
            return NotImplemented
        return self._minute < other._minute

    def __eq__(self, other: "TimePoint") -> bool:
        if not isinstance(other, TimePoint):
            return NotImplemented
        return self._minute == other._minute

    def add_minutes(self, minutes: int) -> "TimePoint":
        new_minute = self._minute + minutes
        if not (0 <= new_minute < 1440):
            raise ValueError("Resulting TimePoint crosses day boundary")
        return TimePoint(new_minute)
