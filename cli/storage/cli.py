import sys
from commands.add_task import run as add_task
from commands .list_task import run as list_tasks


def main():
    if len(sys.argv) < 2: #Ensures that there is atleast one command 
        print("usage: sts <command> ")
        return

    cmd = sys.argv[1]

    if cmd  == "add-task":
        add_task()
    elif cmd == "list-tasks":
        list_tasks()
    else:
        print(f"Uknown command: {cmd}")


if __name__ == "__main__":
    main() 