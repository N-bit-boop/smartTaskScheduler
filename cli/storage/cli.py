import sys
from commands.add_task import run as add_task


def main():
    if len(sys.argv) < 2: #Ensures that there is atleast one command 
        print("usage: sts <command> ")
        return

    cmd = sys.argv[1]

    if cmd  == "add-task":
        add_task()
    else:
        print(f"Uknown command: {cmd}")


if __name__ == "__main__":
    main() 