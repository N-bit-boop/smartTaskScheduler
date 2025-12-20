from timecore.time_rep import TimePoint
from dataclasses import dataclass

@dataclass(frozen=True)

class TimeInterval:
    start: TimePoint
    end: TimePoint

    def __post_init__ (self):
        if self.start >= self.end:
            raise ValueError("Strat must come before the end ")
    
    def duration(self) -> int :
        return self.end.minute - self.start.minute
    
    def overlaps(self, other: "TimeInterval") -> bool:
        return not (self.end <= other.start or other.end <= self.start)
    
    #If self starts after but ends before
    def contains(self, other: "TimeInterval") ->bool:
        return self.start <= other.start and other.end <= self.end
    
    #Self in this case is the total free time in the day, other serves as blocks 
    def subtract(self, other: "TimeInterval") -> list["TimeInterval"]:
        if not self.overlaps(other):
            return [self]
        
        result = []

        if self.start < other.start:
            result.append(TimeInterval(self.start, other.start))
        
        if other.end < self.end:
            result.append(TimeInterval(other.end, self.end))

        return result     
