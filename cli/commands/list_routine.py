from cli.storage.routines_store import load_routines

WEEKDAYS = ["Mon,tue,wed,thur,fri,sat, sun"]

def mask_to_days(mask: int ) -> str:
    days = []
    for i, name in enumerate(WEEKDAYS):
        if mask & (1 << i):
            days.append(name)
    return ",".join(days)


def run():
     routines = load_routines()

     if not routines:
        print("No routines are found")
        return
     
     print ("\nRoutines\n")


     for i, r in enumerate(routines,start=1):
        h = r.start_time.minute() // 60
        m =r.start_time.minute() %  60
        
        print(f"[{i}] {r.name}")
        print(f"    Start: {h:02d}:{m:02d}")
        print(f"    Duration: {r.duration} min")
        print(f"    Days: {mask_to_days(r.recurrence)}")
        print(f"    Protected: {'yes'}")