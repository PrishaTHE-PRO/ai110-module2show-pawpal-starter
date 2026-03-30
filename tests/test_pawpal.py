import pytest
from pawpal_system import Task, Pet, Owner, Scheduler


# --- Task ---

def test_task_mark_complete():
    task = Task(title="Walk", duration_minutes=20, priority="high")
    task.mark_complete()
    assert task.completed is True


def test_task_reschedule():
    task = Task(title="Walk", duration_minutes=20, priority="high", scheduled_time="08:00")
    task.reschedule("10:00")
    assert task.scheduled_time == "10:00"


def test_task_next_occurrence_daily():
    task = Task(title="Walk", duration_minutes=20, priority="high",
                frequency="daily", scheduled_time="08:00")
    next_task = task.next_occurrence()
    assert next_task is not None
    assert next_task.scheduled_time == "08:00"
    assert next_task.completed is False


def test_task_next_occurrence_no_frequency():
    task = Task(title="Walk", duration_minutes=20, priority="high")
    assert task.next_occurrence() is None


# --- Pet ---

def test_pet_add_and_get_tasks():
    pet = Pet(name="Mochi", species="dog")
    task = Task(title="Walk", duration_minutes=20, priority="high")
    pet.add_task(task)
    assert len(pet.get_tasks()) == 1


def test_pet_remove_task():
    pet = Pet(name="Mochi", species="dog")
    pet.add_task(Task(title="Walk", duration_minutes=20, priority="high"))
    pet.remove_task("Walk")
    assert pet.get_tasks() == []


def test_pet_get_pending_tasks():
    pet = Pet(name="Mochi", species="dog")
    done = Task(title="Bath", duration_minutes=30, priority="low")
    done.mark_complete()
    pending = Task(title="Walk", duration_minutes=20, priority="high")
    pet.add_task(done)
    pet.add_task(pending)
    assert pet.get_pending_tasks() == [pending]


# --- Owner ---

def test_owner_add_and_get_all_tasks():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    pet.add_task(Task(title="Walk", duration_minutes=20, priority="high"))
    owner.add_pet(pet)
    assert len(owner.get_all_tasks()) == 1


def test_owner_remove_pet():
    owner = Owner(name="Jordan")
    owner.add_pet(Pet(name="Mochi", species="dog"))
    owner.remove_pet("Mochi")
    assert owner.pets == []


def test_owner_get_pending_tasks_across_pets():
    owner = Owner(name="Jordan")
    dog = Pet(name="Mochi", species="dog")
    cat = Pet(name="Luna", species="cat")
    dog.add_task(Task(title="Walk", duration_minutes=20, priority="high"))
    cat.add_task(Task(title="Feed", duration_minutes=5, priority="high"))
    owner.add_pet(dog)
    owner.add_pet(cat)
    assert len(owner.get_pending_tasks()) == 2


# --- Scheduler ---

def test_scheduler_generate_schedule_order():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    pet.add_task(Task(title="Walk",  duration_minutes=20, priority="high",   scheduled_time="08:00"))
    pet.add_task(Task(title="Bath",  duration_minutes=30, priority="low",    scheduled_time="07:00"))
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    schedule = scheduler.generate_daily_schedule()
    times = [t.scheduled_time for t in scheduler.sort_by_time(schedule)]
    assert times == sorted(times)


def test_scheduler_no_conflicts():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    pet.add_task(Task(title="Walk", duration_minutes=20, priority="high",   scheduled_time="08:00"))
    pet.add_task(Task(title="Feed", duration_minutes=10, priority="medium", scheduled_time="09:00"))
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    schedule = scheduler.generate_daily_schedule()
    assert scheduler.detect_conflicts(schedule) == []


def test_scheduler_detects_conflict():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    pet.add_task(Task(title="Walk", duration_minutes=60, priority="high",   scheduled_time="08:00"))
    pet.add_task(Task(title="Bath", duration_minutes=30, priority="medium", scheduled_time="08:30"))
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    schedule = scheduler.generate_daily_schedule()
    conflicts = scheduler.detect_conflicts(schedule)
    assert len(conflicts) == 1


def test_scheduler_mark_task_complete_recurring():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    task = Task(title="Walk", duration_minutes=20, priority="high",
                frequency="daily", scheduled_time="08:00")
    pet.add_task(task)
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    scheduler.mark_task_complete(task)
    assert task.completed is True
    pending = pet.get_pending_tasks()
    assert len(pending) == 1
    assert pending[0].title == "Walk"


def test_scheduler_filter_by_status():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    done = Task(title="Bath", duration_minutes=30, priority="low", scheduled_time="07:00")
    done.mark_complete()
    active = Task(title="Walk", duration_minutes=20, priority="high", scheduled_time="08:00")
    pet.add_task(done)
    pet.add_task(active)
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    all_tasks = owner.get_all_tasks()
    assert scheduler.filter_tasks(all_tasks, status="pending") == [active]
    assert scheduler.filter_tasks(all_tasks, status="completed") == [done]
