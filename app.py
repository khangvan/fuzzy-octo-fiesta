"""Main Streamlit application for scheduling optimization demo."""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass
from typing import List

import streamlit as st


st.set_page_config(page_title="Scheduling Optimizer", layout="wide")


@dataclass
class Task:
    """Simple representation of a task in the schedule."""

    name: str
    hours: float
    due_date: dt.date | None


@dataclass
class ParseResult:
    """Represents parsed tasks and any validation errors."""

    tasks: List[Task]
    errors: List[str]


def parse_tasks(raw_text: str) -> ParseResult:
    """Parse newline separated tasks.

    Each line should follow the format: "task name | hours | YYYY-MM-DD(optional)".
    Any lines that cannot be parsed will be skipped and surfaced as warnings.
    """

    tasks: List[Task] = []
    errors: List[str] = []
    for line_no, line in enumerate(raw_text.splitlines(), start=1):
        if not line.strip():
            continue

        parts = [part.strip() for part in line.split("|")]
        if not parts[0]:
            errors.append(f"Line {line_no}: Task name is required.")
            continue

        try:
            hours = float(parts[1]) if len(parts) > 1 and parts[1] else 1.0
        except ValueError:
            errors.append(f"Line {line_no}: Hours must be a number (got '{parts[1]}').")
            continue

        due = None
        if len(parts) > 2 and parts[2]:
            try:
                due = dt.datetime.strptime(parts[2], "%Y-%m-%d").date()
            except ValueError:
                errors.append(
                    f"Line {line_no}: Due date must be YYYY-MM-DD (got '{parts[2]}')."
                )
                continue

        tasks.append(Task(name=parts[0], hours=hours, due_date=due))

    return ParseResult(tasks=tasks, errors=errors)


def distribute_tasks(tasks: List[Task], hours_per_day: float) -> List[tuple[str, List[Task]]]:
    """Greedy distribution of tasks across days.

    Tasks exceeding the daily capacity are still assigned to their own day so the
    suggestion always completes every task.
    """

    if not tasks:
        return []

    scheduled: List[tuple[str, List[Task]]] = []
    day_index = 0
    remaining = hours_per_day
    current_day: List[Task] = []

    for task in tasks:
        too_large_for_day = task.hours > hours_per_day
        if (task.hours > remaining and current_day) or too_large_for_day:
            scheduled.append((f"Day {day_index + 1}", current_day))
            current_day = []
            day_index += 1
            remaining = hours_per_day

        current_day.append(task)
        remaining -= task.hours

        if too_large_for_day:
            scheduled.append((f"Day {day_index + 1}", current_day))
            current_day = []
            day_index += 1
            remaining = hours_per_day

    if current_day:
        scheduled.append((f"Day {day_index + 1}", current_day))

    return scheduled


def main() -> None:
    st.title("Scheduling Optimizer")
    st.write(
        "Use this lightweight interface to explore how tasks can be distributed across"
        " multiple days based on an estimated number of hours available."
    )

    with st.sidebar:
        st.header("Configuration")
        hours_available = st.slider("Hours per day", min_value=1, max_value=12, value=6)
        st.caption(
            "Adjust the slider to see how the schedule changes when the daily capacity"
            " increases or decreases."
        )

    default_tasks = """Design review | 2 | 2024-07-01
Prototype API | 4 | 2024-06-25
Write documentation | 3
Team sync | 1 | 2024-06-20
QA pass | 2"""

    task_text = st.text_area(
        "Tasks",
        default_tasks,
        help="Provide one task per line using 'name | hours | YYYY-MM-DD(optional)'.",
    )

    parsed = parse_tasks(task_text)
    if parsed.errors:
        st.warning("\n".join(parsed.errors))

    tasks_sorted = sorted(
        parsed.tasks,
        key=lambda task: task.due_date or dt.date.max,
    )

    if tasks_sorted:
        st.subheader("Task backlog")
        st.dataframe(
            {
                "Task": [task.name for task in tasks_sorted],
                "Hours": [task.hours for task in tasks_sorted],
                "Due": [task.due_date.isoformat() if task.due_date else "—" for task in tasks_sorted],
            },
            use_container_width=True,
        )

    schedule = distribute_tasks(tasks_sorted, hours_available)

    if not schedule:
        st.info("Add a task to see the generated schedule.")
        return

    st.subheader("Suggested Schedule")
    for day, day_tasks in schedule:
        daily_total = sum(task.hours for task in day_tasks)
        st.markdown(f"### {day} — {daily_total}h")
        for task in day_tasks:
            due = task.due_date.isoformat() if task.due_date else "No due date"
            st.write(f"- **{task.name}** — {task.hours}h (Due: {due})")


if __name__ == "__main__":
    main()

