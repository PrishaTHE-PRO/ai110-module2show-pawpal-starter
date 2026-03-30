# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
 -> Task: represents a pet car activity with attributes like title, duration, and priority. Its responsibility is to store task-related data.
 -> Pet: stores information about the pet (name, species) and maintains a list of tasks associated with that pet.
 -> Owner: represents the user and includes preferences such as available time or scheduling constraints.
 -> Scheduler: Acts as the "brain" that retrieves tasks from pets, organizes them based on constraints, detects conflicts, and produces a daily plan.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

During implementation, three meaningful changes emerged from the initial UML:

1. **`detect_conflicts()` return type changed from `list[tuple]` to `list[str]`** — the initial design returned raw `(Task, Task)` pairs, which required the UI to format its own messages. Returning pre-formatted warning strings kept the UI thin and the logic testable in isolation.

2. **`next_occurrence()` moved from time-only to full calendar dates** — the original version shifted an `HH:MM` string by a timedelta (producing the same time, not a different day). The fix combined `date.today() + timedelta` with `datetime.combine()` so daily tasks actually land tomorrow and weekly tasks land next week. This required both `sort_by_time()` and `detect_conflicts()` to handle two time formats (`HH:MM` and `YYYY-MM-DD HH:MM`).

3. **`Scheduler → Task` arrow removed from UML** — the initial diagram showed a direct Scheduler-to-Task relationship. In practice the scheduler only ever talks to the Owner and receives Task objects back through `get_pending_tasks()`. The direct arrow was misleading and was removed.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?
The Scheduler considers:
-> Available time in the day
-> Task duration
-> Task priority (low, medium, high)
-> High-priority tasks are always scheduled first, while low-priority tasks are only added if time allows. This ensures essential pet care is never missed.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The system only flags conflicts for exact time matches rather than overlapping durations. This simplifies the algorithm and avoids overwhelming the user with warnings. While it may miss some subtle overlaps, it keeps the schedule clear and understandable.
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used VS Code Claude to:

Brainstorm class structure and relationships
Generate Python dataclass skeletons
Suggest scheduling algorithms (sorting, filtering, conflict detection)
Draft test cases for key behaviors

Prompts that asked claude to translate UML to code or simplify algorithms were especially effective.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

At one point, claude suggested an overly complex Scheduler with multiple layers of abstraction. I rejected it because it added unnecessary complexity. I verified this by comparing readability, testability, and project scope.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested:

Task addition and completion updates
Task sorting by time
Recurring task creation
Conflict detection for overlapping tasks

These tests ensured that the Scheduler behaved predictably and core pet care tasks were properly handled.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I am confident in the system’s correctness for standard scenarios. Additional edge cases I would test include pets with no tasks, multiple tasks at the same time, and tasks longer than the available day.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

Separation between UI and logic worked very well, allowing me to build and test the backend independently.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would enhance the Scheduler to account for time-of-day preferences and partial overlaps between tasks. Recurrence handling could also be more flexible (e.g., weekly or custom intervals).

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

Good system design relies on clear separation of responsibilities, and AI is most effective when used as a collaborative assistant rather than a replacement. Being the "lead architect" means making final design decisions while using AI to explore options, draft code, and refine logic efficiently.
