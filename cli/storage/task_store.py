import json
from pathlib import Path
from typing import List, Optional

from domain.tasks import Task
from timecore.time_rep import TimePoint

TASKS_PATH = Path("data/tasks.json")
TASKS_PATH.parent.mkdir(parents=True, exist_ok=True)


PRIORITY_MIN = 1 
PRIORITY_MAX = 5 

#decompose the task
def _task_to_dict(task: Task) -> dict:
    return {
        "identifier": task.identifier,
        "duration": task.duration,
        "priority": task.priority,
        "droppable": task.droppable,
        "deadline": (
            f"{task.deadline.minute() // 60:02d}:{task.deadline.minute() % 60:02d}"
            if task.deadline is not None
            else None
        ),
    }


def _dict_to_task(data: dict) -> Task:
    try:
        identifier = data["identifier"]
        duration = data["duration"]
        priority = data["priority"]
        droppable = data["droppable"]
        deadline_raw = data.get("deadline")
    except KeyError as e:
        raise ValueError(f"Missing field: {e}")

    # Identifier
    if not isinstance(identifier, str) or not identifier.strip():
        raise ValueError("Task identifier must be a non-empty string")

    # Duration
    if not isinstance(duration, int) or duration <= 0:
        raise ValueError("Task duration must be a positive integer")

    # Priority
    if not isinstance(priority, int) or not (PRIORITY_MIN <= priority <= PRIORITY_MAX):
        raise ValueError("Task priority out of range")

    # Droppable
    if not isinstance(droppable, bool):
        raise ValueError("Task droppable must be boolean")

    # Deadline
    deadline: Optional[TimePoint]
    if deadline_raw is None:
        deadline = None
    elif isinstance(deadline_raw, str):
        try:
            hour, minute = map(int, deadline_raw.split(":"))
            deadline = TimePoint(hour * 60 + minute)
        except Exception:
            raise ValueError(f"Invalid deadline format: {deadline_raw}")
    else:
        raise ValueError("Deadline must be string or null")

    return Task(
        identifier=identifier,
        duration=duration,
        priority=priority,
        droppable=droppable,
        deadline=deadline,
    )

#Load tasks from disk and ensure that all are valid 
def load_tasks() -> List[Task]:
    if not TASKS_PATH.exists():
        return []
    
    try:
        content = TASKS_PATH.read_text(encoding="utf-8").strip()
        if not content:
            return []   

        raw = json.loads(content)

    except json.JSONDecodeError as e:
        raise ValueError("Malformed tasks.json") from e

    if not isinstance(raw, list):
        raise ValueError("tasks.json must contain a list")

    tasks: List[Task] = []
    seen_ids = set()

    for entry in raw:
        task = _dict_to_task(entry)
        if task.identifier in seen_ids:
            raise ValueError(f"Duplicate task identifier: {task.identifier}")
        seen_ids.add(task.identifier)
        tasks.append(task)

    return tasks


def save_tasks(tasks: List[Task]) -> None:
    data = [_task_to_dict(task) for task in tasks]

    with TASKS_PATH.open("w", encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def add_task(task:Task) -> None:
    tasks = load_tasks()

    if any(t.identifier == task.identifier for t in tasks ):
        raise ValueError(f"Duplicate task identifier: {task.identifier}")
    
    tasks.append(task)
    save_tasks(tasks)



def remove_task(identifier: str) -> bool:
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t.identifier != identifier]

    if len(new_tasks) == len(tasks):
        return False
    
    save_tasks(new_tasks)

    return True