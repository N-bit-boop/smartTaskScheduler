from cli.storage.task_store import load_tasks,remove_task


def run(arg: str ):
    try:
        tasks = load_tasks()

        if not tasks:
            print("No tasks left to remove")
            return
         
        identifier = arg

        if arg.isdigit(): # allows for index and string identification
            idx = int(arg) - 1
            if not(0 <= idx < len(tasks)):
                print("Invalid task number")
                return
            identifier = tasks[idx].identifier

        removed = remove_task(identifier)
        
        if removed:
            print(f"removed task: {identifier}")
        else:
            print(f"task not found: {identifier}")
    except Exception as e:
        print(f"erorr {e}")