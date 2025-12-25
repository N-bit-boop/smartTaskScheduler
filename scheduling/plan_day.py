from timecore.intervals import TimeInterval
from domain.routines import Routine
from calendarss.modelss import CalendarEvent
from domain.tasks import Task
from calendarss.adapter import calendar_toBlocked
from calendarss.routine_adapter import routine_adapter 
from scheduling.availability import availability
from scheduling.planner import resolve_deadlines
from scheduling.planner import place_tasks
from datetime import date, datetime
from timecore.time_rep import TimePoint

def plan_day(*, window: TimeInterval, weekday: int, tasks: list[Task], routines: list[Routine], calendar_events: list[CalendarEvent]):

    warnings: list[str] = []
    explanations: list[str] = [] 

    blocked_calender = calendar_toBlocked(calendar_events, window)

    blocked_routine = routine_adapter(window, routines, weekday)

    #Total blocked time
    blocked = blocked_calender + blocked_routine

    free = availability(window, blocked)

    if not free:
        warnings.append("No free time in this window")

    planning_date = date.today()  # or pass this into plan_day explicitly

    deadlineT = []
    non_deadlineT = []

    for task in tasks:
        if task.deadline is None:
            non_deadlineT.append(task)
            continue

        # Convert absolute deadline → TimePoint if it applies today
        if isinstance(task.deadline, datetime):
            if task.deadline.date() != planning_date:
                continue  # deadline not today
            tp = TimePoint(task.deadline.hour * 60 + task.deadline.minute)

        elif isinstance(task.deadline, date):
            if task.deadline != planning_date:
                continue
            tp = TimePoint(23 * 60 + 59)  # end of day

        # Attach derived TimePoint just for planning
        task._deadline_tp = tp
        deadlineT.append(task)

     # Resolve deadlines (this COMMITs deadline tasks)
    (
        feasible,
        free_after_deadlines,
        scheduled_deadlines,
        remaining_non_deadline_tasks,
        dropped_tasks,
        infeasible_tasks,
    ) = resolve_deadlines(
        free,
        deadlineT,
        non_deadlineT,
    )


    # Place ONLY non-deadline tasks
    scheduled_optional = place_tasks(
        free_after_deadlines,
        remaining_non_deadline_tasks,
    )

    # Final schedule
    scheduled = scheduled_deadlines + scheduled_optional

    return {
        "scheduled": scheduled,
        "dropped": dropped_tasks,
        "infeasible": infeasible_tasks,
        "warnings": warnings,
        "explanations": explanations,
    }

def _deadline_for_day(task: Task, planning_date: date) -> TimePoint | None:
    """
    Convert a task's absolute deadline into a TimePoint constraint
    for THIS planning day.
    """
    if task.deadline is None:
        return None

    # date-only deadline
    if isinstance(task.deadline, date) and not isinstance(task.deadline, datetime):
        if task.deadline < planning_date:
            return TimePoint(0)        # overdue
        if task.deadline > planning_date:
            return None               # not due today
        return TimePoint(1439)        # end of day

    # datetime deadline
    if isinstance(task.deadline, datetime):
        if task.deadline.date() != planning_date:
            return None
        return TimePoint(task.deadline.hour * 60 + task.deadline.minute)

    return None
     