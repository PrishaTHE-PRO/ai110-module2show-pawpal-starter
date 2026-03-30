import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

# --- Persistent state ---
# st.session_state acts like a dictionary that survives reruns.
# The "not in" check ensures we only create the Owner once per session,
# not on every button click or page refresh.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="")

owner = st.session_state.owner

# --- Owner setup ---
st.subheader("Owner & Pet Setup")
owner_name = st.text_input("Owner name", value=owner.name or "Jordan")
owner.name = owner_name

pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    existing = [p.name for p in owner.pets]
    if pet_name and pet_name not in existing:
        owner.add_pet(Pet(name=pet_name, species=species))
        st.success(f"Added {pet_name} the {species}.")
    elif pet_name in existing:
        st.warning(f"{pet_name} is already added.")

if owner.pets:
    st.write("Pets:", ", ".join(p.name for p in owner.pets))

# --- Task entry ---
st.markdown("### Tasks")
col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
with col4:
    assigned_pet = st.selectbox("Assign to pet", [p.name for p in owner.pets] or ["(add a pet first)"])

if st.button("Add task"):
    target = next((p for p in owner.pets if p.name == assigned_pet), None)
    if target:
        target.add_task(Task(title=task_title, duration_minutes=int(duration), priority=priority))
        st.success(f"Added '{task_title}' to {assigned_pet}.")
    else:
        st.error("Add a pet first before adding tasks.")

all_tasks = owner.get_all_tasks()
if all_tasks:
    st.write("Current tasks:")
    st.table([
        {"pet": next(p.name for p in owner.pets if t in p.tasks),
         "title": t.title, "duration_minutes": t.duration_minutes, "priority": t.priority}
        for t in all_tasks
    ])
else:
    st.info("No tasks yet. Add a pet and task above.")

st.divider()

# --- Schedule generation ---
st.subheader("Build Schedule")

if st.button("Generate schedule"):
    if not owner.pets or not owner.get_pending_tasks():
        st.warning("Add at least one pet and one task first.")
    else:
        scheduler = Scheduler(owner)
        schedule = scheduler.generate_daily_schedule()
        conflicts = scheduler.detect_conflicts(schedule)

        st.success(f"Scheduled {len(schedule)} task(s) for {owner.name}.")
        st.table([
            {"time": t.scheduled_time, "task": t.title,
             "duration (min)": t.duration_minutes, "priority": t.priority}
            for t in scheduler.sort_by_time(schedule)
        ])

        if conflicts:
            st.error(f"{len(conflicts)} conflict(s) detected:")
            for a, b in conflicts:
                st.write(f"- **{a.title}** ({a.scheduled_time}) overlaps **{b.title}** ({b.scheduled_time})")
        else:
            st.info("No scheduling conflicts.")
