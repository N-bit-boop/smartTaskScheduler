from timecore.time_rep import TimePoint
from typing import Optional, Union
from datetime import date, datetime

class Task:
    def __init__(self, identifier: str, duration: int, priority: int, deadline: Optional[Union[date,datetime]] = None, droppable: bool = True):

        if not isinstance(identifier, str) or not identifier:
            raise TypeError("Must be a non mepty string")
        self.identifier = identifier

        if not isinstance(duration, int) or duration <= 0:
            raise TypeError("Must be a non zero integer")
        self.duration = duration
        
        if not isinstance(priority, int):
            raise TypeError("Must be a non zero integer")
        self.priority = priority

        if deadline is not None and not isinstance(deadline, (date, datetime)):
            raise TypeError("Deadline must be a date, datetime, or None")
        self.deadline = deadline

        
        # Droppable: boolean
        if not isinstance(droppable, bool):
            raise TypeError("Droppable must be a boolean")
        self.droppable = droppable

    def __repr__(self):
        return (f"Task({self.identifier!r}, duration={self.duration}, "
                f"priority={self.priority}, deadline={self.deadline}, droppable={self.droppable})")