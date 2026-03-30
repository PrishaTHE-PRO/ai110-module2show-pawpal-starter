# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Features

- **Multi-pet support** — add multiple pets and assign tasks to each independently
- **Priority-based scheduling** — high-priority tasks are always placed first; untimed tasks are auto-assigned times sequentially after timed ones
- **Chronological sorting** — `sort_by_time()` uses `datetime.strptime` with a lambda key to handle both `HH:MM` (today) and `YYYY-MM-DD HH:MM` (recurring future) formats
- **Conflict detection** — `detect_conflicts()` uses interval intersection to find overlapping task windows and surfaces human-readable warnings in the UI before the day starts
- **Recurring tasks** — marking a `daily` or `weekly` task complete automatically queues the next occurrence using `date.today() + timedelta`, attached to the correct pet
- **Task filtering** — filter the task list by pet name, completion status, or both
- **Owner preferences** — configurable day start time and max tasks per day cap the generated schedule
- **26 automated tests** — covers happy paths and edge cases (empty pets, exact-time conflicts, missing scheduled times)

## 📸 Demo

![PawPal App](Screenshot 2026-03-29 at 9.51.06 PM.png)

## Smarter Scheduling

The `Scheduler` class in `pawpal_system.py` goes beyond a simple task list with four key algorithms:

- **Sorting** — `sort_by_time()` uses a `lambda` key with `datetime.strptime` to sort tasks chronologically, handling both `HH:MM` (today's tasks) and `YYYY-MM-DD HH:MM` (future recurring tasks) formats.
- **Filtering** — `filter_tasks()` accepts an optional `status` (`"pending"` / `"completed"`) and `pet_name` to return a targeted subset of tasks across all pets.
- **Conflict detection** — `detect_conflicts()` uses interval intersection (`a_start < b_end and b_start < a_end`) to find overlapping tasks and returns human-readable warning strings instead of crashing.
- **Recurring tasks** — `mark_task_complete()` calls `next_occurrence()` on any task with a `frequency`, which uses `date.today() + timedelta` to schedule the next real calendar date (`daily` → +1 day, `weekly` → +7 days) and re-queues it on the correct pet.

## Testing PawPal+

Run the full test suite with:

```bash
python -m pytest
```

The suite contains **26 tests** across four classes:

| Area | What's covered |
|---|---|
| `Task` | mark complete, reschedule, daily/weekly recurrence, no-frequency returns None, missing time defaults |
| `Pet` | add/get/remove tasks, pending filter, edge case: pet with no tasks |
| `Owner` | add/remove pets, flatten tasks across multiple pets, edge case: owner with no pets |
| `Scheduler` | schedule ordering, chronological sort, unscheduled tasks sort last, filter by status and pet name, overlap conflict detection, exact-same-start-time conflict, warning strings (not tuples), recurring re-queue, one-off tasks don't re-queue, empty schedule |

**Confidence level: ★★★★☆**
Core scheduling behaviors are fully covered. The remaining gap is date-boundary edge cases for recurring tasks (e.g. tasks crossing midnight or spanning multiple days).

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
