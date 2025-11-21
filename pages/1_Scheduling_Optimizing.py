"""Streamlit page dedicated to scheduling optimization tips."""

from __future__ import annotations

import streamlit as st


st.set_page_config(page_title="Scheduling Optimizing", layout="wide")


def main() -> None:
    st.title("Scheduling Optimizing")
    st.write(
        "This page provides guidance and interactive controls for planning a more"
        " effective schedule."
    )

    st.subheader("Optimization Goals")
    goals = {
        "Balanced Workload": "Distribute tasks so that no single day is overloaded.",
        "Deadline Driven": "Prioritize items with the earliest deadline first.",
        "Focus Blocks": "Group similar work together to reduce context switching.",
    }
    for title, description in goals.items():
        st.markdown(f"- **{title}** — {description}")

    st.subheader("What-if Analysis")
    tasks = st.number_input("Number of tasks", min_value=1, value=5)
    avg_hours = st.slider("Average hours per task", 1, 8, 3)
    capacity = st.slider("Daily capacity (hours)", 1, 12, 6)

    total_hours = tasks * avg_hours
    estimated_days = round(total_hours / capacity + 0.499)

    st.metric("Total effort", f"{total_hours} hours")
    st.metric("Estimated days", estimated_days)

    st.info(
        "Use this simple what-if calculator to see how adjusting the number of tasks"
        " or daily capacity affects your delivery timeline."
    )


if __name__ == "__main__":
    main()

