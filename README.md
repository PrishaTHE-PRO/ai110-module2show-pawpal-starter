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

## Smarter Scheduling

The `Scheduler` class in `pawpal_system.py` goes beyond a simple task list with four key algorithms:

- **Sorting** — `sort_by_time()` uses a `lambda` key with `datetime.strptime` to sort tasks chronologically, handling both `HH:MM` (today's tasks) and `YYYY-MM-DD HH:MM` (future recurring tasks) formats.
- **Filtering** — `filter_tasks()` accepts an optional `status` (`"pending"` / `"completed"`) and `pet_name` to return a targeted subset of tasks across all pets.
- **Conflict detection** — `detect_conflicts()` uses interval intersection (`a_start < b_end and b_start < a_end`) to find overlapping tasks and returns human-readable warning strings instead of crashing.
- **Recurring tasks** — `mark_task_complete()` calls `next_occurrence()` on any task with a `frequency`, which uses `date.today() + timedelta` to schedule the next real calendar date (`daily` → +1 day, `weekly` → +7 days) and re-queues it on the correct pet.

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
