import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("PawPal+")
st.caption("A smart daily planner for pet owners.")

# ── Persistent session state ──────────────────────────────────────────────────
# The "not in" guard ensures the Owner is created once per session, not on
# every Streamlit rerun triggered by a button click or widget interaction.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="")

owner = st.session_state.owner

# ── Section 1: Owner & Pet Setup ──────────────────────────────────────────────
st.header("1. Owner & Pet Setup")

owner.name = st.text_input("Owner name", value=owner.name or "Jordan")

col_pet, col_species, col_btn = st.columns([2, 2, 1])
with col_pet:
    pet_name = st.text_input("Pet name", value="Mochi")
with col_species:
    species = st.selectbox("Species", ["dog", "cat", "rabbit", "other"])
with col_btn:
    st.write("")
    st.write("")
    if st.button("Add pet"):
        existing = [p.name for p in owner.pets]
        if pet_name and pet_name not in existing:
            owner.add_pet(Pet(name=pet_name, species=species))
            st.success(f"Added {pet_name} the {species}.")
        elif pet_name in existing:
            st.warning(f"{pet_name} is already in your list.")
        else:
            st.error("Enter a pet name first.")

if owner.pets:
    st.info(f"Pets: {', '.join(p.name for p in owner.pets)}")

st.divider()

# ── Section 2: Add Tasks ──────────────────────────────────────────────────────
st.header("2. Add Tasks")

if not owner.pets:
    st.info("Add a pet above before adding tasks.")
else:
    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning Walk")
        assigned_pet = st.selectbox("Assign to", [p.name for p in owner.pets])
    with col2:
        duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
        priority = st.selectbox("Priority", ["high", "medium", "low"])
    with col3:
        sched_time = st.text_input("Scheduled time (HH:MM)", value="", placeholder="e.g. 08:00")
        frequency = st.selectbox("Repeat", ["none", "daily", "weekly"])

    if st.button("Add task"):
        target = next((p for p in owner.pets if p.name == assigned_pet), None)
        if target:
            target.add_task(Task(
                title=task_title,
                duration_minutes=int(duration),
                priority=priority,
                scheduled_time=sched_time.strip() or None,
                frequency=frequency if frequency != "none" else None,
            ))
            st.success(f"Added '{task_title}' to {assigned_pet}.")

    # Current task list with filter controls
    all_tasks = owner.get_all_tasks()
    if all_tasks:
        st.markdown("#### Current Tasks")
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            filter_pet = st.selectbox("Filter by pet", ["All"] + [p.name for p in owner.pets],
                                      key="filter_pet")
        with f_col2:
            filter_status = st.selectbox("Filter by status", ["All", "pending", "completed"],
                                         key="filter_status")

        scheduler_preview = Scheduler(owner)
        filtered = scheduler_preview.filter_tasks(
            all_tasks,
            status=filter_status if filter_status != "All" else None,
            pet_name=filter_pet if filter_pet != "All" else None,
        )

        if filtered:
            rows = []
            for t in filtered:
                pet_label = next((p.name for p in owner.pets if t in p.tasks), "?")
                rows.append({
                    "Pet": pet_label,
                    "Task": t.title,
                    "Time": t.scheduled_time or "unscheduled",
                    "Duration (min)": t.duration_minutes,
                    "Priority": t.priority,
                    "Repeat": t.frequency or "—",
                    "Status": "Done" if t.completed else "Pending",
                })
            st.table(rows)
        else:
            st.info("No tasks match the current filter.")
    else:
        st.info("No tasks added yet.")

st.divider()

# ── Section 3: Generate Schedule ──────────────────────────────────────────────
st.header("3. Today's Schedule")

col_pref1, col_pref2 = st.columns(2)
with col_pref1:
    start_time_pref = st.text_input("Day starts at (HH:MM)", value="08:00")
with col_pref2:
    max_tasks_pref = st.number_input("Max tasks per day", min_value=1, max_value=20, value=8)

if st.button("Generate Schedule", type="primary"):
    if not owner.pets or not owner.get_pending_tasks():
        st.warning("Add at least one pet and one pending task before generating a schedule.")
    else:
        owner.preferences["start_time"] = start_time_pref
        owner.preferences["max_tasks_per_day"] = int(max_tasks_pref)

        scheduler = Scheduler(owner)
        schedule = scheduler.generate_daily_schedule()
        sorted_schedule = scheduler.sort_by_time(schedule)
        conflicts = scheduler.detect_conflicts(schedule)

        # Summary metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Tasks scheduled", len(schedule))
        m2.metric("Conflicts found", len(conflicts))
        m3.metric("Pets covered", len({
            p.name for p in owner.pets
            if any(t in p.tasks for t in schedule)
        }))

        # Conflict warnings — shown before the table so the owner sees them first
        if conflicts:
            st.error(f"{len(conflicts)} scheduling conflict(s) detected — review before your day starts:")
            for warning in conflicts:
                st.warning(warning)
        else:
            st.success("No scheduling conflicts — your day is clear!")

        # Sorted schedule table
        st.markdown("#### Schedule (sorted by time)")
        schedule_rows = []
        for t in sorted_schedule:
            pet_label = next((p.name for p in owner.pets if t in p.tasks), "?")
            schedule_rows.append({
                "Time": t.scheduled_time or "unscheduled",
                "Pet": pet_label,
                "Task": t.title,
                "Duration (min)": t.duration_minutes,
                "Priority": t.priority,
                "Repeat": t.frequency or "—",
            })
        st.table(schedule_rows)

        # Mark complete buttons
        st.markdown("#### Mark a task complete")
        pending_tasks = [(t, next((p.name for p in owner.pets if t in p.tasks), "?"))
                         for t in schedule if not t.completed]
        if pending_tasks:
            task_options = {f"{pet} — {t.title} ({t.scheduled_time or 'unscheduled'})": t
                            for t, pet in pending_tasks}
            selected_label = st.selectbox("Select task", list(task_options.keys()))
            if st.button("Mark complete"):
                selected_task = task_options[selected_label]
                scheduler.mark_task_complete(selected_task)
                if selected_task.frequency:
                    next_t = next(
                        (t for p in owner.pets for t in p.tasks
                         if t.title == selected_task.title and not t.completed),
                        None
                    )
                    msg = f"Next occurrence scheduled: {next_t.scheduled_time}" if next_t else ""
                    st.success(f"Marked '{selected_task.title}' complete! {msg}")
                else:
                    st.success(f"Marked '{selected_task.title}' complete!")
        else:
            st.info("All scheduled tasks are already complete.")
