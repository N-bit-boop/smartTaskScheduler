from timecore.intervals import TimeInterval

def normalize(base: TimeInterval, blocked: list[TimeInterval]) -> list[TimeInterval]:
    normalize = []
    
    #Makes sure it is within base frame 
    for b in blocked:
        if not b.overlaps(base):
            continue

            #Process of clipping to ensure that the block exists within the work day 
        start = max(b.start, base.start)
        #Does not extend past the workday
        end = min(b.end, base.end)
        normalize.append(TimeInterval(start,end))
    return normalize

def availability(base: TimeInterval, blocked: list[TimeInterval]) -> list[TimeInterval]:
    blocked = normalize(base, blocked)
    blocked.sort(key=lambda b:b.start)

    free = [base]

    for block in blocked:
        next_free = [] #Temp list to store all the free times 
        for interval in free:
            next_free.extend(interval.subtract(block))
        free = next_free
    return free