from datetime import datetime, date, time
from typing import List, Tuple

from googleapiclient.errors import HttpError

from domain.tasks import Task
from timecore.intervals import TimeInterval
from calendarss.google_auth import get_cal_service
from zoneinfo import ZoneInfo


def write_events(scheduled: List[Tuple[Task, TimeInterval]], day: date, calendar_id: str = "primary", dry_run:bool = True):
    """
    Write scheduled tasks into google calendar -->dry_run printts what is writetn
    """

    service = get_cal_service()
    LOCAL_TZ = ZoneInfo("America/Toronto")

    for task, interval in scheduled:
        start_dt = datetime.combine(day,time(hour=interval.start.minute() // 60, minute=interval.start.minute() % 60), tzinfo=LOCAL_TZ,)
        end_dt = datetime.combine(day,time(hour=interval.end.minute() // 60, minute=interval.end.minute() % 60), tzinfo=LOCAL_TZ,)

        event_body = {
            "summary": task.identifier,
            "description" : "[STS]",
             "start": {
                "dateTime": start_dt.isoformat(),
                "timeZone": "America/Toronto",
            },
            "end": {
                "dateTime": end_dt.isoformat(),
                "timeZone": "America/Toronto",
            },
        }  


        if dry_run:
            print(
                f"[DRY-RUN] Would create event: "
                f"{task.identifier} "
                f"{start_dt.strftime('%H:%M')}–{end_dt.strftime('%H:%M')}"
            )
            continue

        try:
            service.events().insert(
                calendarId=calendar_id,
                body=event_body
            ).execute()

            print(
                f"[CREATED] {task.identifier} "
                f"{start_dt.strftime('%H:%M')}–{end_dt.strftime('%H:%M')}"
            )

        except HttpError as err:
            print(f"[ERROR] Failed to create event for {task.identifier}: {err}")
        