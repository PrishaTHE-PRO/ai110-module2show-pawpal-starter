from pawpal_system import Task, Pet, Owner, Scheduler

# --- Setup ---
owner = Owner(name="Jordan", preferences={"start_time": "07:00", "max_tasks_per_day": 6})

mochi = Pet(name="Mochi", species="dog")
luna = Pet(name="Luna", species="cat")

# Tasks for Mochi
mochi.add_task(Task(title="Morning Walk",    duration_minutes=30, priority="high",   scheduled_time="07:00"))
mochi.add_task(Task(title="Evening Walk",    duration_minutes=20, priority="medium", scheduled_time="18:00"))
mochi.add_task(Task(title="Flea Treatment",  duration_minutes=10, priority="low",    frequency="weekly"))

# Tasks for Luna
luna.add_task(Task(title="Feeding",          duration_minutes=5,  priority="high",   scheduled_time="08:00"))
luna.add_task(Task(title="Litter Box Clean", duration_minutes=10, priority="medium", scheduled_time="09:00"))
luna.add_task(Task(title="Playtime",         duration_minutes=15, priority="low"))

owner.add_pet(mochi)
owner.add_pet(luna)

# --- Schedule ---
scheduler = Scheduler(owner)
schedule = scheduler.generate_daily_schedule()

# --- Print ---
print("=" * 40)
print("       TODAY'S SCHEDULE — PawPal+")
print("=" * 40)
for task in scheduler.sort_by_time(schedule):
    pet_name = next(
        (p.name for p in owner.pets if task in p.tasks), "Unknown"
    )
    status = "✓" if task.completed else "•"
    print(f"  {status} {task.scheduled_time}  [{pet_name}]  {task.title} ({task.duration_minutes} min) — {task.priority} priority")

conflicts = scheduler.detect_conflicts(schedule)
print("=" * 40)
if conflicts:
    print("⚠ Conflicts detected:")
    for a, b in conflicts:
        print(f"  {a.title} ({a.scheduled_time}) overlaps with {b.title} ({b.scheduled_time})")
else:
    print("  No scheduling conflicts.")
print("=" * 40)
