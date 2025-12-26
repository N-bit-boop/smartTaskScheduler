# scheduling/planner.py
from __future__ import annotations
from datetime import date
from math import inf
from typing import List, Tuple

from timecore.time_rep import TimePoint
from timecore.intervals import TimeInterval
from domain.tasks import Task


def _days_until_deadline(task: Task, day: date) -> float:
    if task.deadline is None:
        return inf
    return (task.deadline - day).days


def _task_sort_key(task: Task, day: date):
    # Earlier deadline first, then higher priority (smaller number first)
    return (_days_until_deadline(task, day), task.priority)


def find_slot(task: Task, free_intervals: List[TimeInterval]) -> TimeInterval:
    for interval in free_intervals:
        available_minutes = interval.end.minute() - interval.start.minute()
        if available_minutes >= task.duration:
            start_minute = interval.start.minute()
            end_minute = start_minute + task.duration
            return TimeInterval(TimePoint(start_minute), TimePoint(end_minute))
    raise ValueError("No valid slot found")


def subtract_interval(free_intervals: List[TimeInterval], assigned: TimeInterval) -> List[TimeInterval]:
    result: List[TimeInterval] = []
    for interval in free_intervals:
        result.extend(interval.subtract(assigned))
    return result


def schedule_tasks(
    *,
    free_intervals: List[TimeInterval],
    tasks: List[Task],
    day: date,
) -> Tuple[List[Tuple[Task, TimeInterval]], List[Task], List[Task]]:
    """
    Returns: (scheduled, dropped, infeasible)

    dropped   = droppable tasks that didn’t fit
    infeasible = non-droppable tasks that didn’t fit
    """
    scheduled: List[Tuple[Task, TimeInterval]] = []
    dropped: List[Task] = []
    infeasible: List[Task] = []

    for task in sorted(tasks, key=lambda t: _task_sort_key(t, day)):
        try:
            assigned = find_slot(task, free_intervals)
        except ValueError:
            if task.droppable:
                dropped.append(task)
            else:
                infeasible.append(task)
            continue

        scheduled.append((task, assigned))
        free_intervals = subtract_interval(free_intervals, assigned)

    return scheduled, dropped, infeasible
