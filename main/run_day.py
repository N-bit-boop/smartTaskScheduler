# run_day.py
import datetime
from timecore.time_rep import TimePoint
from timecore.intervals import TimeInterval
from calendarss.google_reader import read_events
from scheduling.plan_day import plan_day
from domain.tasks import Task
from domain.routines import Routine  
from datetime import timezone
from calendarss.google_write import write_events
from cli.storage.task_store import load_tasks

def main():
    #Choose the planning date
    date = datetime.date.today()  # Hard-coded today for MVP

    # Build Google fetch window (datetimes)
    start_dt = datetime.datetime.combine(date, datetime.time.min)
    end_dt   = datetime.datetime.combine(date + datetime.timedelta(days=1), datetime.time.min)


    #xplicit timezone 
    start_dt = start_dt.replace(tzinfo=timezone.utc)
    end_dt   = end_dt.replace(tzinfo=timezone.utc)


    #Build scheduling window (planner working hours)
    window = TimeInterval(
        TimePoint(9 * 60),   # 09:00
        TimePoint(17 * 60)   # 17:00
    )

    # Read Google Calendar events
    try:
        calendar_events = read_events(start_dt, end_dt)
    except Exception as e:
        print("WARNING: Could not fetch Google events:", e)
        calendar_events = []

    # Load tasks and routines (MVP: hard-coded)
    tasks = load_tasks()

    if not tasks:
        print("No tasks found. Add tasks using sts add-task")

    routines = [
        Routine(name="Gym", start_time=TimePoint(7*60), duration=60, recurrence=0b1111100),  # Mon-Fri
        Routine(name="Lunch", start_time=TimePoint(12*60), duration=60, recurrence=0b1111111),  # Daily
        
    ]

    # Call plan_day
    proposal = plan_day(
        window=window,
        weekday=date.weekday(),
        tasks=tasks,
        routines=routines,
        calendar_events=calendar_events
    )

    # Display results
    if proposal["warnings"]:
        print("WARNINGS:")
        for w in proposal["warnings"]:
            print("-", w)

    
    print("\nScheduled tasks:")
    for task, interval in proposal["scheduled"]:
        print(f"{interval.start}–{interval.end}  {task.identifier}")

    #  Dropped tasks
    if proposal["dropped"]:
        print("\nDropped tasks:")
        for t in proposal["dropped"]:
            print("-", t.identifier)

    #  Infeasible tasks
    if proposal.get("infeasible"):
        print("\nInfeasible tasks:")
        for t in proposal["infeasible"]:
            print("-", t.identifier)

    #  Explanations
    if proposal.get("explanations"):
        print("\nExplanations:")
        for exp in proposal["explanations"]:
            print("-", exp)
    
    confirm = input("\nWrite this schedule to Google Calendar? (y/n): ").strip().lower()

    if confirm == "y":
        write_events(
            scheduled=proposal["scheduled"],
            day=date,
            dry_run=False,   # 🔴 REAL WRITE
        )
    else:
        print("Schedule not written.")

if __name__ == "__main__":
    main()