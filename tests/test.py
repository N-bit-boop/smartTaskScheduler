from timecore.time_rep import TimePoint
from timecore.intervals import TimeInterval
from domain.tasks import Task
from scheduling.availability import availability
from scheduling.planner import (
    resolve_deadlines,
    place_tasks,
    produce_proposal
)

# -----------------------------
# Helpers
# -----------------------------
def tp(h, m=0):
    return TimePoint(h * 60 + m)


def run_test(name, base, blocked, tasks):
    print(f"\n=== {name} ===")

    # Compute free time
    free = availability(base, blocked)

    # Separate tasks
    deadline_tasks = [t for t in tasks if t.deadline]
    non_deadline_tasks = [t for t in tasks if not t.deadline]

    # Resolve deadlines (hard constraints)
    ok, free, deadline_tasks, non_deadline_tasks, dropped_deadline = resolve_deadlines(
        free, deadline_tasks, non_deadline_tasks
    )

    if not ok:
        print("❌ Infeasible (deadlines cannot be satisfied)")
        print("Dropped:", [t.identifier for t in dropped_deadline])
        return

    # Place optional tasks (best-effort)
    schedule = place_tasks(free, deadline_tasks, non_deadline_tasks)

    # -----------------------------
    # PRESENTATION LOGIC (IMPORTANT)
    # -----------------------------
    scheduled_ids = {task.identifier for task, _ in schedule}

    dropped_optional = [
        t.identifier for t in non_deadline_tasks
        if t.identifier not in scheduled_ids
    ]

    # Output
    if schedule:
        print("✅ Schedule:")
        for task, interval in schedule:
            print(f"  {task.identifier}: {interval.start} → {interval.end}")
    else:
        print("✅ Schedule:")
        print("  (deadlines satisfied, no optional tasks fit)")

    print("Dropped:", dropped_optional)


# =============================
# TEST CASE — MULTIPLE DROPS
# =============================
if __name__ == "__main__":

    run_test(
        "Scenario 11: explicit multiple drops",
        base=TimeInterval(tp(9), tp(17)),
        blocked=[],
        tasks=[
            # Deadline task consumes almost entire day
            Task("A", 450, priority=1, deadline=tp(16, 30)),  # 7.5 hours

            # All optional tasks too large for remaining 30 minutes
            Task("B", 60, priority=2),
            Task("C", 90, priority=3),
            Task("D", 120, priority=4),
        ]
    )
