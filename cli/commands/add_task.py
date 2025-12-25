from domain.tasks import Task
from timecore.time_rep import TimePoint
from cli.storage.task_store import add_task

def prompt(msg: str) -> str:
    return input(msg).strip()

def parse_deadline(raw: str):
    if not raw:
        return None

    try:
        parts = raw.split(":")
        if len(parts) != 2:
            raise ValueError

        h, m = map(int, parts)
        if not (0 <= h < 24 and 0 <= m < 60):
            raise ValueError

        return TimePoint(h * 60 + m)

    except Exception:
        raise ValueError("Deadline must be in HH:MM (24-hour) format")


def parse_droppable(raw: str) -> bool:
    raw = raw.lower()
    if raw in ("y", "yes"):
        return True
    if raw in ("n", "no"):
        return False
    raise ValueError("Droppable must be y/n")


def run():
    try:
        identifier = prompt("Task name: ")
        if not identifier:
            raise ValueError("Task name cannot be empty")

        duration = int(prompt("Duration (minutes): "))
        priority = int(prompt("Priority (1–5): "))

        deadline_raw = prompt("Deadline (HH:MM or blank): ")
        droppable_raw = prompt("Droppable? (y/n): ")

        deadline = parse_deadline(deadline_raw)
        droppable = parse_droppable(droppable_raw)

        task = Task(
            identifier=identifier.strip(),
            duration=duration,
            priority=priority,
            deadline=deadline,
            droppable=droppable,
        )

        add_task(task)

        print("\n✔ Task added:")
        print(f"  Name: {task.identifier}")
        print(f"  Duration: {task.duration} minutes")
        print(f"  Priority: {task.priority}")
        print(f"  Deadline: {deadline if deadline else 'none'}")
        print(f"  Droppable: {'yes' if droppable else 'no'}")

    except Exception as e:
        print(f"\n Error: {e}")