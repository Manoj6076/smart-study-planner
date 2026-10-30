import datetime as dt

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Smart Study Planner",
    page_icon="📚",
    layout="wide"
)

if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "next_id" not in st.session_state:
    st.session_state.next_id = 1


def get_priority(exam_date, completed):
    if completed:
        return "Completed"

    days_left = (exam_date - dt.date.today()).days

    if days_left <= 1:
        return "High"
    elif days_left <= 3:
        return "High"
    elif days_left <= 7:
        return "Medium"
    return "Low"


def get_days_left(exam_date):
    return (exam_date - dt.date.today()).days


st.title("📚 Smart Study Planner")
st.write(
    "Plan your study sessions, prioritize upcoming exams, "
    "and track your learning progress."
)

st.info(
    "Add your subjects and topics, set exam dates, "
    "then generate a daily plan."
)

# Sidebar: daily study capacity
st.sidebar.header("⚙️ Study Settings")
available_hours = st.sidebar.number_input(
    "Available study hours per day",
    min_value=1,
    max_value=16,
    value=4,
    step=1
)

st.sidebar.caption(
    "The daily plan uses your available hours "
    "to allocate time to pending topics."
)

# Add a study topic
st.header("1. Add a Study Topic")

with st.form("add_task_form", clear_on_submit=True):
    subject = st.text_input(
        "Subject",
        placeholder="e.g. Machine Learning"
    )
    topic = st.text_input(
        "Topic to study",
        placeholder="e.g. Decision Trees"
    )
    exam_date = st.date_input(
        "Exam date",
        value=dt.date.today() + dt.timedelta(days=7),
        min_value=dt.date.today()
    )
    study_hours = st.number_input(
        "Estimated study time (hours)",
        min_value=0.5,
        max_value=20.0,
        value=1.0,
        step=0.5
    )

    add_clicked = st.form_submit_button(
        "➕ Add Topic",
        type="primary"
    )

    if add_clicked:
        if not subject.strip() or not topic.strip():
            st.error("Please enter both a subject and a topic.")
        else:
            st.session_state.tasks.append({
                "ID": st.session_state.next_id,
                "Subject": subject.strip(),
                "Topic": topic.strip(),
                "Exam Date": exam_date,
                "Study Hours": float(study_hours),
                "Completed": False
            })
            st.session_state.next_id += 1
            st.success("Topic added successfully!")
            st.rerun()

tasks = st.session_state.tasks

# Progress overview
st.header("2. Your Study Dashboard")

if not tasks:
    st.info("No topics added yet. Add your first topic above.")
else:
    total = len(tasks)
    completed_count = sum(t["Completed"] for t in tasks)
    pending_count = total - completed_count
    progress = completed_count / total

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Topics", total)
    col2.metric("Pending Topics", pending_count)
    col3.metric("Completed Topics", completed_count)

    st.progress(progress)
    st.write(f"Overall completion: **{progress:.0%}**")

    records = []
    for task in tasks:
        records.append({
            "ID": task["ID"],
            "Subject": task["Subject"],
            "Topic": task["Topic"],
            "Exam Date": task["Exam Date"],
            "Days Left": get_days_left(task["Exam Date"]),
            "Study Hours": task["Study Hours"],
            "Priority": get_priority(
                task["Exam Date"], task["Completed"]
            ),
            "Status": (
                "Completed" if task["Completed"] else "Pending"
            )
        })

    df = pd.DataFrame(records)

    st.subheader("All Topics")
    st.dataframe(
        df.drop(columns=["ID"]),
        use_container_width=True,
        hide_index=True
    )

    st.subheader("3. Update Topic Progress")

    task_options = {
        f'{t["ID"]} — {t["Subject"]}: {t["Topic"]}': t["ID"]
        for t in tasks
    }

    with st.form("update_task_form"):
        selected_label = st.selectbox(
            "Choose a topic",
            list(task_options.keys())
        )
        selected_status = st.radio(
            "Set status",
            ["Pending", "Completed"],
            horizontal=True
        )
        update_clicked = st.form_submit_button("Save Status")

        if update_clicked:
            selected_id = task_options[selected_label]
            for task in st.session_state.tasks:
                if task["ID"] == selected_id:
                    task["Completed"] = (
                        selected_status == "Completed"
                    )
                    break
            st.success("Progress updated!")
            st.rerun()

    st.subheader("4. Generate Today's Study Plan")

    if st.button("🗓️ Generate Daily Plan", type="primary"):
        pending_tasks = [
            t for t in tasks if not t["Completed"]
        ]

        pending_tasks.sort(
            key=lambda t: (
                get_days_left(t["Exam Date"]),
                -t["Study Hours"]
            )
        )

        remaining_minutes = int(available_hours * 60)
        plan = []

        for task in pending_tasks:
            if remaining_minutes <= 0:
                break

            requested_minutes = int(task["Study Hours"] * 60)
            allocated_minutes = min(
                requested_minutes, remaining_minutes
            )

            if allocated_minutes > 0:
                plan.append({
                    "Subject": task["Subject"],
                    "Topic": task["Topic"],
                    "Priority": get_priority(
                        task["Exam Date"], False
                    ),
                    "Study Minutes": allocated_minutes
                })
                remaining_minutes -= allocated_minutes

        if plan:
            st.dataframe(
                pd.DataFrame(plan),
                use_container_width=True,
                hide_index=True
            )
            st.caption(
                f"Planned {sum(p['Study Minutes'] for p in plan)} "
                f"minutes out of {available_hours * 60} available."
            )
            if remaining_minutes == 0:
                st.info(
                    "Your available study time is fully allocated. "
                    "Some topics may need to be continued tomorrow."
                )
        else:
            st.success(
                "No pending topics! Add a topic or enjoy your free time."
            )

    st.subheader("5. Progress by Subject")

    chart_data = (
        pd.DataFrame(tasks)
        .groupby("Subject")
        .agg(
            Total=("Topic", "count"),
            Completed=("Completed", "sum")
        )
    )

    chart_data["Pending"] = (
        chart_data["Total"] - chart_data["Completed"]
    )

    st.bar_chart(chart_data[["Completed", "Pending"]])

    st.subheader("6. Export Your Study Tasks")

    export_df = pd.DataFrame(records).drop(columns=["ID"])
    csv_data = export_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Download Study Plan as CSV",
        data=csv_data,
        file_name="my_study_plan.csv",
        mime="text/csv"
    )

    if st.button("🗑️ Clear All Topics"):
        st.session_state.tasks = []
        st.rerun()

st.divider()
st.caption(
    "Smart Study Planner | A student productivity project "
    "built with Python and Streamlit."
)
