# Smart Task Scheduler (STS)

A personal scheduling system that intelligently plans your day by combining tasks, routines, and Google Calendar events.  
STS automatically allocates work into available time using greedy scheduling, respects deadlines and priorities, and can sync schedules directly to Google Calendar.

This project was built with a strong focus on **software architecture, correctness, and extensibility**, rather than UI-first shortcuts.

---

## ✨ Features

### Core Scheduling
- Greedy interval-based scheduling of tasks  
- Deadline-aware prioritization (earlier deadlines scheduled first)  
- Priority-based ordering for optional tasks  
- Automatic conflict resolution using interval subtraction  
- Detection of infeasible or dropped tasks  

### Domain Modeling
- **Tasks**: duration, priority, droppable flag, optional deadline  
- **Routines**: recurring weekly blocks (e.g., gym, lunch)  
- **Calendar events**: imported as immutable blocked intervals  
- Strong separation between domain, scheduling logic, and adapters  

### Google Calendar Integration
- Read existing events to block unavailable time  
- Write scheduled tasks back to Google Calendar  
- Update existing STS events instead of duplicating  
- Automatically delete orphaned STS events  
- Safe dry-run mode before writing  

### CLI Interface
- Add, list, and remove tasks  
- Add, list, and remove routines  
- Plan a specific day from the command line  
- Optional confirmation before writing to Google Calendar  

---

## 🧠 Scheduling Strategy (High Level)

STS uses a **greedy interval sweep algorithm**:

1. Collect all blocked time:
   - Google Calendar events  
   - User-defined routines  
2. Compute free intervals via interval subtraction  
3. Schedule deadline tasks first (earliest deadline first)  
4. Commit intervals immediately (greedy)  
5. Schedule remaining tasks by priority  
6. Drop optional tasks only if necessary  

This approach is:
- **Deterministic**  
- **Efficient**  
- **Easy to reason about**  
- **Extensible** to future heuristics (PERT, chunking, learning)  

---

## 📂 Project Structure

```text
STS/
├── domain/
│   ├── tasks.py          # Task model
│   ├── routines.py       # Routine model
│
├── timecore/
│   ├── time_rep.py       # TimePoint abstraction
│   └── intervals.py      # TimeInterval logic
│
├── scheduling/
│   ├── availability.py   # Free-time computation
│   ├── planner.py        # Core scheduling logic
│   └── plan_day.py       # Daily orchestration
│
├── calendarss/
│   ├── google_reader.py  # Read Google Calendar events
│   ├── google_write.py   # Write/update/delete events
│   ├── adapter.py        # Calendar → intervals
│   └── routine_adapter.py
│
├── cli/
│   ├── cli.py            # Command router
│   ├── commands/         # add-task, list-task, etc.
│   └── storage/
│       ├── task_store.py
│       └── routine_store.py
│
├── main/
│   └── run_day.py        # End-to-end execution
│
├── data/
│   ├── tasks.json
│   └── routines.json
│
└── README.md
```

## 🚀 Features

- Task scheduling with deadlines, durations, priorities, and time windows  
- Daily and recurring routines  
- Automatic conflict-free planning  
- Google Calendar integration  
- Non-destructive calendar sync  
- Infeasible task detection  
- CLI-based workflow  

---



## 📦 Setup

### 1. Create and activate a virtual environment

```bash
python -m venv venv
```
Activate it:

# macOS / Linux
```bash

source venv/bin/activate
```

# Windows
```bash
venv\Scripts\activate
```
Install dependencies:

```bash
pip install google-api-python-client google-auth google-auth-oauthlib
```

### 2. Google Calendar API Setup
STS uses Google OAuth to sync schedules to your calendar.

Go to Google Cloud Console

Create a new project

Enable the Google Calendar API

Create OAuth credentials

Download the file named credentials.json

Place credentials.json in the project root

On the first run, your browser will open to authorize access to your Google Calendar.

## 🧪 Usage
Run all commands from the project root.

# Add a Task
```bash
python -m cli.cli add-task
```
# List Tasks
```bash
python -m cli.cli list-tasks
```
#Remove a Task
```bash
python -m cli.cli remove-task <task-id>
```
# Add a Routine
```bash
python -m cli.cli add-routine
```
# Generate and Schedule the Day
```bash
python -m main.run_day
```
You will be asked for confirmation before any events are written to Google Calendar.

## 🔄 Google Calendar Sync Rules
STS is designed to never interfere with events you did not create.

Events created by STS are internally tagged

Previously scheduled STS events are updated, not duplicated

Tasks removed from STS are deleted from Google Calendar

Non-STS calendar events are never modified or deleted

This ensures your personal and external calendar events are always safe.


