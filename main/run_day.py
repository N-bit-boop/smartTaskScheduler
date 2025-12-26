# main/run_day.py
import datetime
from datetime import timezone

from timecore.time_rep import TimePoint
from timecore.intervals import TimeInterval
from calendarss.google_reader import read_events
from scheduling.plan_day import plan_day
from calendarss.google_write import write_events

from cli.storage.task_store import load_tasks
from cli.storage.routines_store import load_routines  

def main():
    day = datetime.date.today()

    start_dt = datetime.datetime.combine(day, datetime.time.min).replace(tzinfo=timezone.utc)
    end_dt = datetime.datetime.combine(day + datetime.timedelta(days=1), datetime.time.min).replace(tzinfo=timezone.utc)

    window = TimeInterval(TimePoint(9 * 60), TimePoint(17 * 60))

    try:
        calendar_events = read_events(start_dt, end_dt)
    except Exception as e:
        print("WARNING: Could not fetch Google events:", e)
        calendar_events = []

    tasks = load_tasks()
    routines = load_routines()

    proposal = plan_day(
        window=window,
        day=day,
        weekday=day.weekday(),
        tasks=tasks,
        routines=routines,
        calendar_events=calendar_events,
    )

    print("\nScheduled tasks:")
    for task, interval in proposal["scheduled"]:
        print(f"{interval.start}–{interval.end}  {task.identifier}")

    if proposal["dropped"]:
        print("\nDropped tasks:")
        for t in proposal["dropped"]:
            print("-", t.identifier)

    if proposal["infeasible"]:
        print("\nInfeasible tasks:")
        for t in proposal["infeasible"]:
            print("-", t.identifier)

    confirm = input("\nWrite this schedule to Google Calendar? (y/n): ").strip().lower()
    if confirm == "y":
        write_events(scheduled=proposal["scheduled"], day=day, dry_run=False)
    else:
        print("Schedule not written.")


if __name__ == "__main__":
    main()
