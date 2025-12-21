from timecore.intervals import TimeInterval
from domain.routines import Routine
from calendarss.modelss import CalendarEvent
from domain.tasks import Task
from calendarss.adapter import calendar_toBlocked
from calendarss.routine_adapter import routine_adapter 
from scheduling import availability
from scheduling.planner import resolve_deadlines
from scheduling.planner import place_tasks

def plan_day(*, window: TimeInterval, weekday: int, tasks: list[Task], routines: list[Routine], calendar: list[CalendarEvent]):

    warnings = list[str]
    explanations = list[str] 

    blocked_calender = calendar_toBlocked(calendar, window)

    blocked_routine = routine_adapter(window, routines, weekday)

    #Total blocked time
    blocked = blocked_calender + blocked_routine

    free = availability(window, blocked)

    if not free:
        warnings.append("No free time in this window")

    deadlineT = []

    non_deadlineT = []

    for task in tasks:
        if task.deadline is not None:
            deadlineT.append(task)
        else:
            non_deadlineT.append(task)


     # STEP 4 — Resolve deadlines (this COMMITs deadline tasks)
    (
        feasible,
        free_after_deadlines,
        remaining_non_deadline_tasks,
        dropped_tasks,
        infeasible_tasks,
        resolution_explanations,
    ) = resolve_deadlines(
        free,
        deadlineT,
        non_deadlineT,
    )

    explanations.extend(resolution_explanations)

    # STEP 5 — Place ONLY non-deadline tasks
    scheduled = place_tasks(
        free_after_deadlines,
        remaining_non_deadline_tasks,
    )

    # STEP 6 — Proposal
    return {
        "scheduled": scheduled,
        "dropped": dropped_tasks,
        "infeasible": infeasible_tasks,
        "warnings": warnings,
        "explanations": explanations,
    }
     