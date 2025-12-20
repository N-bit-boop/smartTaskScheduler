from timecore.intervals import TimeInterval
from model import CalendarEvent
from typing import Iterable, List

def calendar_toBlocked(events: Iterable[CalendarEvent], window: TimeInterval) ->list[TimeInterval]:

    #Given calendar events and a planning window,
    #return the portions of those events that block time within the window
       
    blocked: list[TimeInterval] = []

    for event in events:
        interval  = event.to_interval()

        if not interval.overlaps(window):
            continue

        #clip to the og planning window 
        start = max(interval.start, window.start)
        end = min(interval.end, window.end)

        blocked.append(TimeInterval(start, end))
    
    return blocked 


