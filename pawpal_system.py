from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional


PRIORITY_RANK = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str                        # "low", "medium", "high"
    frequency: Optional[str] = None      # "daily", "weekly", or None
    completed: bool = False
    scheduled_time: Optional[str] = None # "HH:MM" format

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True

    def reschedule(self, new_time: str):
        """Update the task's scheduled time to new_time."""
        self.scheduled_time = new_time

    def next_occurrence(self) -> Optional["Task"]:
        """Return a fresh Task for the next recurrence, or None if not recurring."""
        if not self.frequency or not self.scheduled_time:
            return None
        current = datetime.strptime(self.scheduled_time, "%H:%M")
        if self.frequency == "daily":
            next_dt = current + timedelta(days=1)
        elif self.frequency == "weekly":
            next_dt = current + timedelta(weeks=1)
        else:
            return None
        return Task(
            title=self.title,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            frequency=self.frequency,
            scheduled_time=next_dt.strftime("%H:%M"),
        )


@dataclass
class Pet:
    name: str
    species: str
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task):
        """Append a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task_title: str):
        """Remove the task matching task_title from this pet's task list."""
        self.tasks = [t for t in self.tasks if t.title != task_title]

    def get_tasks(self) -> list:
        """Return a copy of all tasks assigned to this pet."""
        return list(self.tasks)

    def get_pending_tasks(self) -> list:
        """Return only incomplete tasks for this pet."""
        return [t for t in self.tasks if not t.completed]


class Owner:
    def __init__(self, name: str, preferences: dict = None):
        self.name = name
        self.pets: list[Pet] = []
        # Supported keys: "max_tasks_per_day" (int), "start_time" (str "HH:MM")
        self.preferences: dict = preferences or {}

    def add_pet(self, pet: Pet):
        """Add a pet to this owner's pet list."""
        self.pets.append(pet)

    def remove_pet(self, pet_name: str):
        """Remove the pet matching pet_name from this owner's pet list."""
        self.pets = [p for p in self.pets if p.name != pet_name]

    def get_all_tasks(self) -> list:
        """Return every task across all of this owner's pets."""
        return [task for pet in self.pets for task in pet.get_tasks()]

    def get_pending_tasks(self) -> list:
        """Return all incomplete tasks across every pet this owner has."""
        return [task for pet in self.pets for task in pet.get_pending_tasks()]


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner
        self.schedule: list[Task] = []

    def generate_daily_schedule(self) -> list[Task]:
        """
        Build a daily plan from all pending tasks.
        - Tasks with a scheduled_time are placed first (sorted by time).
        - Remaining tasks are ordered by priority and assigned times sequentially.
        - Respects owner preference 'max_tasks_per_day' and 'start_time'.
        """
        pending = self.owner.get_pending_tasks()
        max_tasks = self.owner.preferences.get("max_tasks_per_day", len(pending))
        start_time = self.owner.preferences.get("start_time", "08:00")

        timed = sorted(
            [t for t in pending if t.scheduled_time],
            key=lambda t: t.scheduled_time,
        )
        untimed = sorted(
            [t for t in pending if not t.scheduled_time],
            key=lambda t: PRIORITY_RANK.get(t.priority, 99),
        )

        # Assign times to untimed tasks starting after the last timed block
        if timed:
            last = timed[-1]
            cursor = datetime.strptime(last.scheduled_time, "%H:%M") + timedelta(minutes=last.duration_minutes)
        else:
            cursor = datetime.strptime(start_time, "%H:%M")

        for task in untimed:
            task.scheduled_time = cursor.strftime("%H:%M")
            cursor += timedelta(minutes=task.duration_minutes)

        self.schedule = (timed + untimed)[:max_tasks]
        return self.schedule

    def sort_by_time(self, tasks: list) -> list[Task]:
        """Return tasks sorted chronologically by scheduled_time."""
        return sorted(tasks, key=lambda t: t.scheduled_time or "99:99")

    def filter_tasks(
        self,
        tasks: list,
        status: Optional[str] = None,
        pet_name: Optional[str] = None,
    ) -> list[Task]:
        """
        Filter tasks by completion status and/or pet name.
        status: "pending" | "completed" | None (all)
        """
        result = tasks

        if status == "pending":
            result = [t for t in result if not t.completed]
        elif status == "completed":
            result = [t for t in result if t.completed]

        if pet_name:
            pet_task_ids = set()
            for pet in self.owner.pets:
                if pet.name == pet_name:
                    pet_task_ids.update(id(t) for t in pet.tasks)
            result = [t for t in result if id(t) in pet_task_ids]

        return result

    def detect_conflicts(self, tasks: list) -> list[tuple]:
        """
        Return a list of (Task, Task) pairs whose time windows overlap.
        Only considers tasks that have a scheduled_time.
        """
        conflicts = []
        timed = [t for t in tasks if t.scheduled_time]

        for i, a in enumerate(timed):
            a_start = datetime.strptime(a.scheduled_time, "%H:%M")
            a_end = a_start + timedelta(minutes=a.duration_minutes)
            for b in timed[i + 1:]:
                b_start = datetime.strptime(b.scheduled_time, "%H:%M")
                b_end = b_start + timedelta(minutes=b.duration_minutes)
                if a_start < b_end and b_start < a_end:
                    conflicts.append((a, b))

        return conflicts

    def mark_task_complete(self, task: Task):
        """
        Mark a task done. If it recurs, add the next occurrence to the right pet.
        """
        task.mark_complete()
        if task.frequency:
            next_task = task.next_occurrence()
            if next_task:
                for pet in self.owner.pets:
                    if task in pet.tasks:
                        pet.add_task(next_task)
                        break
