from timecore.time_rep import TimePoint
from timecore.intervals import TimeInterval
from domain.tasks import Task



def feasibility(deadline_tasks: list[Task], free_intervals: list[TimeInterval]) -> tuple[bool, list[Task]]:
    simulated_free = list(free_intervals)
    infeasible = []

    for task in sorted(deadline_tasks, key=lambda t: t.deadline.minute()):
        placed = False

        for interval in simulated_free:
            latest_end = task.deadline.minute()
            usable_end = min(interval.end.minute(), latest_end)
            available = usable_end - interval.start.minute()

            if available >= task.duration:
                start = interval.start.minute()
                end = start + task.duration
                assigned = TimeInterval(TimePoint(start), TimePoint(end))

                next_free = []
                for free in simulated_free:
                    next_free.extend(free.subtract(assigned))
                simulated_free = next_free

                placed = True
                break

        if not placed:
            infeasible.append(task)

    return len(infeasible) == 0, infeasible, simulated_free

def resolve_deadlines(free_intervals: list[TimeInterval], deadline_tasks: list[Task], non_deadline_tasks: list[Task]) -> tuple[bool, list[TimeInterval], list[Task], list[Task]]:

    remaining_non_deadline = non_deadline_tasks.copy()
    dropped = []

    while True:
        feasible, infeasible,simulated_free = feasibility(deadline_tasks, free_intervals)
        if feasible:
            return True, simulated_free, deadline_tasks, remaining_non_deadline, dropped

        # Pick lowest-priority droppable non-deadline task
        candidates = [t for t in remaining_non_deadline if t.droppable]
        if not candidates:
            return False, simulated_free, deadline_tasks, remaining_non_deadline, dropped

        task_to_drop = min(candidates, key=lambda t: t.priority)
        remaining_non_deadline.remove(task_to_drop)
        dropped.append(task_to_drop)
        # Dropped tasks free time → no changes to free_intervals needed

def find_slot(task: Task, free_intervals: list[TimeInterval]) -> TimeInterval:
    for interval in free_intervals:
        latest_end = task.deadline.minute() if task.deadline else interval.end.minute()
        usable_end = min(interval.end.minute(), latest_end)
        available_minutes = usable_end - interval.start.minute()

        if available_minutes >= task.duration:
            start_minute = interval.start.minute()
            end_minute = start_minute + task.duration
            return TimeInterval(TimePoint(start_minute), TimePoint(end_minute))

    raise ValueError("No valid slot found (should not happen if feasibility passed)")

def subtract_interval(free_intervals: list[TimeInterval], assigned: TimeInterval) -> list[TimeInterval]:
    result = []
    for interval in free_intervals:
        result.extend(interval.subtract(assigned))
    return result

def place_tasks(free_intervals: list[TimeInterval],non_deadline_tasks: list[Task]) -> list[tuple[Task, TimeInterval]]:

    schedule = []

    for task in sorted(non_deadline_tasks, key=lambda t: t.priority):
        try:
            assigned = find_slot(task, free_intervals)
        except ValueError:
        # Task does not fit --> drop it
            continue
        schedule.append((task, assigned))
        free_intervals = subtract_interval(free_intervals, assigned)

    return schedule


def produce_proposal(schedule, dropped, infeasible=None, warnings=None, explanations=None):
    return {
        "scheduled": schedule,
        "dropped": dropped,
        "infeasible": infeasible or [],
        "warnings": warnings or [],
        "explanations": explanations or []
    }