import datetime
from datetime import timezone

from timecore.time_rep import TimePoint
from timecore.intervals import TimeInterval

from cli.storage.task_store import load_tasks
from calendarss.google_reader import read_events
from calendarss.google_write import write_events
from scheduling.plan_day import plan_day
from domain.routines import Routine


def run():
    print("STS sync started")

    day = datetime.date.today()
    weekday =day.weekday()

    start_dt = datetime.datetime.combine(day, datetime.time.min).replace(tzinfo=timezone.utc)
    end_dt = start_dt + datetime.timedelta(days=1)

    #Window for work

    window = TimeInterval(TimePoint(9*60), TimePoint(21 *60))


    tasks = load_tasks()
    if not tasks:
        print("⚠ No tasks found — calendar will be cleared of STS events")

    # load routine
    routines: list[Routine] = []

   
    calendar_events = read_events(start_dt, end_dt)

    proposal = plan_day(
        window=window,
        weekday=weekday,
        tasks=tasks,
        routines=routines,
        calendar_events=calendar_events,
    )


    for w in proposal["warnings"]:
        print("Warning bruh", w )


    #sync into google calendar 
    write_events(
        scheduled=proposal["scheduled"],
        day=day,
        dry_run=False,  # REAL SYNC
    )

    print("STS Sync complete")