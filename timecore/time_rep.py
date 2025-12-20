from dataclasses import dataclass 
from functools import total_ordering
from datetime import datetime, timedelta, date, time

@total_ordering
@dataclass(frozen=True)
class TimePoint:
    _minute : int

    def __post_init__ (self):
        if self._minute < 0 or self._minute >=1440:
            raise ValueError("Need to fit in one day")
        
        #Getter 
    def minute(self) -> int:
        return self._minute
   
   
    def str(self):
        h = self._minute // 60
        m = self._minute % 60

        return f"{h:02d}:{m:02d}"

    

    
    def __lt__(self, other: "TimePoint") -> bool:
        if not isinstance(other, TimePoint):
            return NotImplemented
        return self._minute < other._minute 

    def __eq__ (self, other: "TimePoint") -> bool:
        if not isinstance(other, TimePoint):
            return NotImplemented
        return self._minute == other._minute 
    
    #Duration can be negative, simply means earlier 
    def duration(self, other: "TimePoint") -> int:
        if not isinstance(other, TimePoint):
            raise TypeError("Expected a timepoint")
        return (other._minute - self._minute)
    
    @staticmethod
    def combine(d: date, tp: "TimePoint") -> datetime:
        #Combine a date and this time-of-day into a concrete datetime.
        h = tp._minute // 60
        m = tp._minute % 60
        return datetime.combine(d, time(hour=h, minute=m))

    @staticmethod
    def add_minutes(dt: datetime, minutes: int) -> datetime:
        #Return a new datetime minutes after dt.
        return dt + timedelta(minutes=minutes)
        
