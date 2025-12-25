from datetime import date, datetime
from typing import Optional, Union


class Task:
    def __init__(self,identifier: str,duration: int,priority: int,deadline: Optional[Union[date, datetime]] = None,droppable: bool = True,):
        if not isinstance(identifier, str) or not identifier:
            raise TypeError("Identifier must be a non-empty string")
        self.identifier = identifier

        if not isinstance(duration, int) or duration <= 0:
            raise TypeError("Duration must be a positive integer")
        self.duration = duration

        if not isinstance(priority, int) or not (1 <= priority <= 5):
            raise TypeError("Priority must be between 1 and 5")
        self.priority = priority

        if deadline is not None and not isinstance(deadline, (date, datetime)):
            raise TypeError("Deadline must be a date, datetime, or None")
        self.deadline = deadline

        if not isinstance(droppable, bool):
            raise TypeError("Droppable must be boolean")
        self.droppable = droppable

    def __repr__(self):
        return (
            f"Task({self.identifier!r}, duration={self.duration}, "
            f"priority={self.priority}, deadline={self.deadline}, "
            f"droppable={self.droppable})"
        )
