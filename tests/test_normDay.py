from timecore.time_rep import TimePoint
from timecore.intervals import TimeInterval
from domain.tasks import Task
from domain.routines import Routine
from calendarss.modelss import CalendarEvent
from scheduling.plan_day import plan_day

def tp(h, m=0):
    return TimePoint(h * 60 + m)

def run_realistic_day():
    print("\n=== REALISTIC DAY TEST ===")

    # Workday window
    window = TimeInterval(tp(9), tp(17))
    weekday = 2  # Wednesday

    # Calendar events (meetings)
    calendar_events = [
        CalendarEvent(tp(9, 30), tp(10, 0), "Daily standup"),
        CalendarEvent(tp(14, 0), tp(15, 0), "Project meeting"),
    ]

    # Routines
    routines = [
        Routine(
            name="Lunch",
            start_time=tp(12),
            duration=60,
            recurrence=0b1111111,
            flexible_minutes=0,
            protected=True,
        ),
    ]

    # Tasks
    tasks = [
        Task(
            identifier="Assignment",
            duration=120,
            priority=1,
            deadline=tp(16),
            droppable=False,
        ),
        Task(
            identifier="Read paper",
            duration=60,
            priority=3,
            droppable=True,
        ),
        Task(
            identifier="Emails",
            duration=30,
            priority=5,
            droppable=True,
        ),
    ]

    proposal = plan_day(
        window=window,
        weekday=weekday,
        tasks=tasks,
        routines=routines,
        calendar_events=calendar_events,
    )

    print("\nScheduled:")
    for task, interval in proposal["scheduled"]:
        print(f"- {interval.start} → {interval.end}  {task.identifier}")

    print("\nDropped:")
    for t in proposal["dropped"]:
        print("-", t.identifier)

    print("\nWarnings:")
    for w in proposal["warnings"]:
        print("-", w)

    print("\nInfeasible:")
    for t in proposal["infeasible"]:
        print("-", t.identifier)


if __name__ == "__main__":
    run_realistic_day()
