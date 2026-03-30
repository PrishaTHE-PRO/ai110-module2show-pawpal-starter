from pawpal_system import Task, Pet, Owner, Scheduler

# --- Setup ---
owner = Owner(name="Jordan", preferences={"start_time": "07:00", "max_tasks_per_day": 6})

mochi = Pet(name="Mochi", species="dog")
luna  = Pet(name="Luna",  species="cat")

# Tasks added OUT OF ORDER intentionally to test sorting
mochi.add_task(Task(title="Evening Walk",    duration_minutes=20, priority="medium", scheduled_time="18:00"))
mochi.add_task(Task(title="Morning Walk",    duration_minutes=30, priority="high",   scheduled_time="07:00"))
mochi.add_task(Task(title="Flea Treatment",  duration_minutes=10, priority="low",    frequency="weekly"))
# Deliberately conflicts with Morning Walk (07:00–07:30)
mochi.add_task(Task(title="Vet Call",        duration_minutes=20, priority="high",   scheduled_time="07:15"))

luna.add_task(Task(title="Litter Box Clean", duration_minutes=10, priority="medium", scheduled_time="09:00"))
luna.add_task(Task(title="Feeding",          duration_minutes=5,  priority="high",   scheduled_time="08:00"))
luna.add_task(Task(title="Playtime",         duration_minutes=15, priority="low"))
# Deliberately conflicts with Litter Box Clean (09:00–09:10)
luna.add_task(Task(title="Grooming",         duration_minutes=15, priority="medium", scheduled_time="09:05"))

owner.add_pet(mochi)
owner.add_pet(luna)

scheduler = Scheduler(owner)

# ── 1. SORTING ────────────────────────────────────────────────
print("=" * 45)
print("  SORTED SCHEDULE (all tasks, by time)")
print("=" * 45)
all_tasks = owner.get_all_tasks()
for t in scheduler.sort_by_time(all_tasks):
    print(f"  {t.scheduled_time or 'unscheduled':>16}  {t.title} ({t.priority})")

# ── 2. FILTERING ─────────────────────────────────────────────
print("\n" + "=" * 45)
print("  FILTER — Mochi's tasks only")
print("=" * 45)
mochi_tasks = scheduler.filter_tasks(all_tasks, pet_name="Mochi")
for t in mochi_tasks:
    print(f"  {t.title} — {t.priority}")

print("\n" + "=" * 45)
print("  FILTER — pending tasks only")
print("=" * 45)
# Mark one task complete first so the filter has something to exclude
luna.tasks[0].mark_complete()
pending = scheduler.filter_tasks(owner.get_all_tasks(), status="pending")
for t in pending:
    print(f"  {t.title} — {'done' if t.completed else 'pending'}")

# ── 3. RECURRING TASK ────────────────────────────────────────
print("\n" + "=" * 45)
print("  RECURRING — mark Flea Treatment complete")
print("=" * 45)
flea_task = next(t for t in mochi.tasks if t.title == "Flea Treatment")
print(f"  Before: {flea_task.title} | completed={flea_task.completed}")
scheduler.mark_task_complete(flea_task)
print(f"  After:  {flea_task.title} | completed={flea_task.completed}")
next_flea = next((t for t in mochi.tasks if t.title == "Flea Treatment" and not t.completed), None)
print(f"  Next occurrence scheduled: {next_flea.scheduled_time if next_flea else 'none'}")

# ── 4. DAILY SCHEDULE + CONFLICT CHECK ───────────────────────
print("\n" + "=" * 45)
print("  TODAY'S SCHEDULE — PawPal+")
print("=" * 45)
schedule = scheduler.generate_daily_schedule()
for t in scheduler.sort_by_time(schedule):
    pet_label = next((p.name for p in owner.pets if t in p.tasks), "?")
    status = "✓" if t.completed else "•"
    print(f"  {status} {t.scheduled_time:>16}  [{pet_label}]  {t.title} ({t.duration_minutes} min) — {t.priority}")

warnings = scheduler.detect_conflicts(schedule)
print("=" * 45)
if warnings:
    print("  Conflicts detected:")
    for msg in warnings:
        print(f"  {msg}")
else:
    print("  No scheduling conflicts.")
print("=" * 45)
