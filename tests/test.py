from timecore.time_rep import TimePoint
from timecore.intervals import TimeInterval
from domain.tasks import Task
from scheduling.availability import availability
from scheduling.planner import (
    feasibility,
    resolve_deadlines,
    place_tasks,
    produce_proposal
)

# Helper: create TimePoint from hours/minutes
def tp(h, m=0):
    return TimePoint(h * 60 + m)

def run_test(name, base, blocked, tasks):
    print(f"\n=== {name} ===")

    free = availability(base, blocked)
    deadline_tasks = [t for t in tasks if t.deadline]
    non_deadline_tasks = [t for t in tasks if not t.deadline]

    ok, free, deadline_tasks, non_deadline_tasks, dropped = resolve_deadlines(
        free, deadline_tasks, non_deadline_tasks
    )

    if not ok:
        print("❌ Infeasible schedule")
        print("Dropped:", [t.identifier for t in dropped])
        return

    # 🔴 NEW: if no free time remains, all remaining optional tasks are dropped
    if not free:
        dropped.extend(non_deadline_tasks)
        print("✅ Schedule:")
        print("  (deadlines satisfied, no optional tasks fit)")
        print("Dropped:", [t.identifier for t in dropped])
        return

    schedule = place_tasks(free, deadline_tasks, non_deadline_tasks)
    proposal = produce_proposal(schedule, dropped)

    print("✅ Schedule:")
    for task, interval in proposal["scheduled"]:
        print(f"  {task.identifier}: {interval.start} → {interval.end}")

    print("Dropped:", [t.identifier for t in dropped])

# =========================
# TEST EXECUTION (IMPORTANT)
# =========================
if __name__ == "__main__":

    # Scenario 1 — Basic success
    run_test(
        "Scenario 1: basic success",
        base=TimeInterval(tp(9), tp(17)),
        blocked=[],
        tasks=[
            Task("A", 60, priority=3),
            Task("B", 120, priority=2),
        ]
    )

    # Scenario 2 — Deadline fits
    run_test(
        "Scenario 2: single deadline",
        base=TimeInterval(tp(9), tp(17)),
        blocked=[],
        tasks=[
            Task("A", 120, priority=1, deadline=tp(12)),
            Task("B", 60, priority=3),
        ]
    )

    # Scenario 3 — Drop low priority
    run_test(
        "Scenario 3: drop to resolve",
        base=TimeInterval(tp(9), tp(12)),
        blocked=[],
        tasks=[
            Task("A", 180, priority=1, deadline=tp(12)),
            Task("B", 60, priority=5),
        ]
    )
