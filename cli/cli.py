import sys
from cli.commands.add_task import run as add_task
from cli.commands .list_task import run as list_tasks
from cli.commands .remove_task import run as remove_task
from cli.commands.sync import run as sync


def main():
    if len(sys.argv) < 2: #Ensures that there is atleast one command 
        print("usage: sts <command> ")
        return

    cmd = sys.argv[1]

    if cmd  == "add":
        add_task()
    elif cmd == "list":
        list_tasks()
    elif cmd == "remove":
        if len(sys.argv) < 3:
            print("usage: sts remove task <name|index>")
            return
        remove_task(sys.argv[2])
    elif cmd == "sync":
        sync()
    else:
        print(f"Uknown command: {cmd}")


if __name__ == "__main__":
    main() 