# scheduling/plan_day.py
from datetime import date

from timecore.intervals import TimeInterval
from domain.routines import Routine
from calendarss.modelss import CalendarEvent
from domain.tasks import Task
from calendarss.adapter import calendar_toBlocked
from calendarss.routine_adapter import routine_adapter
from scheduling.availability import availability
from scheduling.planner import schedule_tasks


def plan_day(
    *,
    window: TimeInterval,
    day: date,
    weekday: int,
    tasks: list[Task],
    routines: list[Routine],
    calendar_events: list[CalendarEvent],
):
    warnings: list[str] = []
    explanations: list[str] = []

    blocked_calendar = calendar_toBlocked(calendar_events, window)
    blocked_routines = routine_adapter(window, routines, weekday)
    blocked = blocked_calendar + blocked_routines

    free = availability(window, blocked)

    if not free:
        warnings.append("No free time in this window")
        return {
            "scheduled": [],
            "dropped": [t for t in tasks if t.droppable],
            "infeasible": [t for t in tasks if not t.droppable],
            "warnings": warnings,
            "explanations": explanations,
        }

    scheduled, dropped, infeasible = schedule_tasks(
        free_intervals=free,
        tasks=tasks,
        day=day,
    )

    return {
        "scheduled": scheduled,
        "dropped": dropped,
        "infeasible": infeasible,
        "warnings": warnings,
        "explanations": explanations,
    }
