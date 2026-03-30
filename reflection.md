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
During implementation, I simplified task management by keeping tasks inside the Pet class instead of a separate task manager. This reduced complexity and made the Scheduler easier to implement. I also adjusted the Scheduler to generate plans without storing state, improving testability.

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

The scheduler uses **interval-based conflict detection** (`a_start < b_end and b_start < a_end`) rather than checking exact start-time matches. This means it correctly catches overlapping durations — for example, a 30-minute walk at 07:00 conflicts with a task starting at 07:15 — but it compares tasks using their `HH:MM` time string without accounting for the calendar date. Two recurring tasks on different days with the same time string could produce a false-positive conflict warning.

This tradeoff is reasonable for a single-day scheduler: most users plan one day at a time, so ignoring the date component keeps the logic simple and fast. A future improvement would store tasks as full `datetime` objects so cross-day comparisons are accurate. For now, returning a human-readable warning string (instead of crashing or silently dropping the task) means the user always sees the problem and can manually reschedule.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
