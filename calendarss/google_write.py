from datetime import datetime, date, time
from typing import List, Tuple

from googleapiclient.errors import HttpError

from domain.tasks import Task
from timecore.intervals import TimeInterval
from calendarss.google_auth import get_cal_service
from zoneinfo import ZoneInfo

from typing import Dict
from datetime import datetime, timedelta

LOCAL_TZ = ZoneInfo("America/Toronto")

def write_events(scheduled: List[Tuple[Task, TimeInterval]], day: date, calendar_id: str = "primary", dry_run:bool = True):
    """
    Write scheduled tasks into google calendar -->dry_run printts what is writetn
    """

    service = get_cal_service()
    existing = get_existing_sts_events(service, day, calendar_id)
    scheduled_ids = {task.identifier for task, _ in scheduled}

    #delete orphaned events 
    to_delete = set(existing.keys()) - scheduled_ids

    for task_id in to_delete:
        event_id = existing[task_id]

        if dry_run:
            print(f"[DRY-RUN] Would delete {task_id}")
            continue

        try:
            service.events().delete(
                calendarId=calendar_id,
                eventId=event_id,
            ).execute()
            print(f"[DELETED] {task_id}")
        except HttpError as err:
            print(f"[ERROR] Failed to delete {task_id}: {err}")

    #create update scheduled tasks 
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
            "extendedProperties": {
            "private": {
            "sts": "1", #Adding id so no duplicates are made
            "sts_task_id": task.identifier,
            "sts_day": day.isoformat(),
             }

           }
        }  


        if task.identifier in existing:
            if dry_run:
                print(f"[DRY-RUN] Would update {task.identifier}")
                continue

            service.events().update(
                calendarId=calendar_id,
                eventId=existing[task.identifier],
                body=event_body,
            ).execute()

            print(f"[UPDATED] {task.identifier}")

        else:
            if dry_run:
                print(f"[DRY-RUN] Would create {task.identifier}")
                continue

            service.events().insert(
                calendarId=calendar_id,
                body=event_body,
            ).execute()

            print(f"[CREATED] {task.identifier}")



def get_existing_sts_events(service, day, calendar_id = "primary") -> Dict[str, str]:
    """
    returns tasks_id --> event_id for sts events 
    """

    LOCAL_TZ = ZoneInfo("America/Toronto")

    start_dt = datetime.combine(day, datetime.min.time(), tzinfo=LOCAL_TZ)
    end_dt = start_dt + timedelta(days=1)
  

    events = (
        service.events()
        .list(
            calendarId=calendar_id,
            timeMin=start_dt.isoformat(),
            timeMax=end_dt.isoformat(),
            singleEvents=True,
            privateExtendedProperty="sts=1",
        )
        .execute()
        .get("items", [])
    )

    mapping = {}

    for e in events: 
        props = e.get("extendedProperties", {}).get("private", {})
        task_id = props.get("sts_task_id")
        if task_id:
            mapping[task_id] = e["id"]
        
    return mapping 
        