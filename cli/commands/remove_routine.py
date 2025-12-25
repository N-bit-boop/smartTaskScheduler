from cli.storage.routines_store import remove_routine


def run():
    name = input("Routine name to remove: ").strip()

    if not name:
        print(" Routine name cannot be empty")
        return

    removed = remove_routine(name)

    if removed:
        print(f" Removed routine: {name}")
    else:
        print(f" No routine found with name: {name}")
