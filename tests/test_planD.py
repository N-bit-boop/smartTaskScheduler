# tests/test_plan_day.py

from timecore.time_rep import TimePoint
from timecore.intervals import TimeInterval
from domain.tasks import Task
from domain.routines import Routine
from calendarss.modelss import CalendarEvent
from scheduling.plan_day import plan_day


def tp(h, m=0):
    """Helper: hours/minutes → TimePoint"""
    return TimePoint(h * 60 + m)


def test_plan_day_basic():
    """
    Scenario:
    - Work window: 09:00–17:00
    - Calendar event: 10:00–11:00
    - Routine: Lunch 12:00–13:00 (daily)
    - Tasks:
        A: deadline 15:00, 2h
        B: optional, 1h
    """

    window = TimeInterval(tp(9), tp(17))
    weekday = 0  # Monday

    calendar_events = [
        CalendarEvent(tp(10), tp(11), description="Meeting"),
    ]

    routines = [
        Routine(
            name="Lunch",
            start_time=tp(12),
            duration=60,
            recurrence=0b1111111,  # every day
        )
    ]

    tasks = [
        Task("A", duration=120, priority=1, deadline=tp(15)),
        Task("B", duration=60, priority=5),
    ]

    proposal = plan_day(
        window=window,
        weekday=weekday,
        tasks=tasks,
        routines=routines,
        calendar_events=calendar_events,
    )

    print("\n=== PLAN DAY RESULT ===")

    print("Scheduled:")
    for task, interval in proposal["scheduled"]:
        print(f"  {task.identifier}: {interval.start} → {interval.end}")

    print("Dropped:", [t.identifier for t in proposal["dropped"]])
    print("Infeasible:", [t.identifier for t in proposal["infeasible"]])
    print("Warnings:", proposal["warnings"])
    print("Explanations:", proposal["explanations"])

    # Minimal assertions
    assert any(task.identifier == "A" for task, _ in proposal["scheduled"])
    assert "No free time" not in proposal["warnings"]
