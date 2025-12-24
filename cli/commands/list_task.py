from cli.storage.task_store import load_tasks


def run():
    try:
        tasks = load_tasks()

        if not tasks:
            print("No tasks found.")
            return

        print("\nTasks:\n")

        for i, task in enumerate(tasks, start=1):
            deadline_str = str(task.deadline) if task.deadline else "none"
            droppable_str = "yes" if task.droppable else "no"

            print(f"[{i}] {task.identifier}")
            print(f"    Duration: {task.duration} min")
            print(f"    Priority: {task.priority}")
            print(f"    Deadline: {deadline_str}")
            print(f"    Droppable: {droppable_str}\n")

    except Exception as e:
        print(f"✖ Error: {e}")
