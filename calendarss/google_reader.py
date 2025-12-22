from datetime import datetime
from typing import List
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from calendarss.modelss import CalendarEvent  # domain object
from calendarss.google_auth import get_cal_service  # the function that returns authorized service
from timecore.time_rep import TimePoint




def read_events(start_dt: datetime, end_dt: datetime, calendar_id: str = "primary") ->List[CalendarEvent]:
    """
    Docstring for read_events
    fetch events from google calendar in the specific window and convert into calendar event objects 
    """

    service = get_cal_service()
    events_list: List[CalendarEvent] = []

    try:
        events_result = (
            service.events()
            .list(
                calendarId=calendar_id,
                timeMin=start_dt.isoformat(),
                timeMax=end_dt.isoformat(),
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        items = events_result.get("items", [])

        for item in items:
            # Skip all-day events (they have 'date' instead of 'dateTime')
            start_raw = item["start"].get("dateTime")
            end_raw = item["end"].get("dateTime")
            if not start_raw or not end_raw:
                continue

            # Convert ISO timestamp to TimePoint (minutes since midnight)
            start_tp = iso_to_timepoint(start_raw)
            end_tp = iso_to_timepoint(end_raw)

            description = item.get("summary", "")

            events_list.append(
                CalendarEvent(
                    start=start_tp,
                    end=end_tp,
                    description=description,
                    source="google",
                )
            )

    except HttpError as err:
        print(f"Google API Error: {err}")
        # Optionally return empty list if API fails
        return []

    return events_list





#Helper fucntion 

def iso_to_timepoint(iso_str:str) ->TimePoint:
    """
    Docstring for iso_to_timepoint
    
    covert ISO 8601 datetime string to TimePoint 
    ignores date, computes minutes within a day 
    """

    dt = datetime.fromisoformat(iso_str)
    minutes = dt.hour * 60 + dt.minute

    return TimePoint(minutes)