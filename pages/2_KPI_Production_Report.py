"""Streamlit page presenting a KPI-oriented production report."""

from __future__ import annotations

import math
from typing import List, TypedDict

import pandas as pd
import streamlit as st


st.set_page_config(page_title="KPI Production Report", layout="wide")


class ProductionRow(TypedDict):
    """Structure describing a single production line/shift record."""

    line: str
    shift: str
    units: int
    target: int
    scrap_pct: float
    downtime_hr: float


def default_rows() -> List[ProductionRow]:
    """Provide seed data that users can customize."""

    return [
        {
            "line": "Line A",
            "shift": "Morning",
            "units": 1200,
            "target": 1100,
            "scrap_pct": 1.4,
            "downtime_hr": 0.5,
        },
        {
            "line": "Line B",
            "shift": "Evening",
            "units": 900,
            "target": 950,
            "scrap_pct": 2.1,
            "downtime_hr": 1.2,
        },
        {
            "line": "Line C",
            "shift": "Night",
            "units": 750,
            "target": 800,
            "scrap_pct": 1.1,
            "downtime_hr": 0.8,
        },
    ]


def safe_ratio(numerator: float, denominator: float) -> float:
    """Avoid division by zero when computing derived KPIs."""

    if math.isclose(denominator, 0.0):
        return 0.0
    return numerator / denominator


def main() -> None:
    st.title("KPI Production Report")
    st.write(
        "Monitor production KPIs for each line/shift, update live values, and review"
        " trends against goals."
    )

    st.subheader("Input data")
    st.caption("Edit any cell to reflect the most recent production run.")
    edited_df = st.data_editor(
        pd.DataFrame(default_rows()),
        num_rows="dynamic",
        use_container_width=True,
    )

    if edited_df.empty:
        st.warning("Add at least one row to generate the KPI report.")
        return

    edited_df["variance"] = edited_df["units"] - edited_df["target"]
    edited_df["attainment"] = edited_df.apply(
        lambda row: safe_ratio(row["units"], row["target"]), axis=1
    )

    total_units = int(edited_df["units"].sum())
    total_target = int(edited_df["target"].sum())
    total_variance = total_units - total_target
    avg_attainment = safe_ratio(total_units, total_target)
    avg_scrap = float(edited_df["scrap_pct"].mean())
    total_downtime = float(edited_df["downtime_hr"].sum())

    st.subheader("Headline KPIs")
    kpi_cols = st.columns(4)
    kpi_cols[0].metric("Total output", f"{total_units:,} units", delta=total_variance)
    kpi_cols[1].metric(
        "Target attainment",
        f"{avg_attainment:.0%}",
        delta=f"{avg_attainment - 1:.1%}",
    )
    kpi_cols[2].metric("Average scrap", f"{avg_scrap:.2f}%")
    kpi_cols[3].metric("Downtime", f"{total_downtime:.1f} hrs")

    st.subheader("Performance by line")
    st.dataframe(
        edited_df[
            [
                "line",
                "shift",
                "units",
                "target",
                "variance",
                "attainment",
                "scrap_pct",
                "downtime_hr",
            ]
        ]
        .rename(
            columns={
                "attainment": "attainment %",
                "scrap_pct": "scrap %",
                "downtime_hr": "downtime (h)",
            }
        )
        .assign(
            **{
                "attainment %": lambda df: (df["attainment %"] * 100).map(
                    "{:.1f}%".format
                ),
                "scrap %": lambda df: df["scrap %"].map("{:.2f}%".format),
                "downtime (h)": lambda df: df["downtime (h)"].map("{:.1f}".format),
            }
        ),
        use_container_width=True,
    )

    st.subheader("Output vs. target")
    chart_df = edited_df.set_index("line")["units"].to_frame("Actual")
    chart_df["Target"] = edited_df.set_index("line")["target"]
    st.bar_chart(chart_df, height=300)

    st.info(
        "This page focuses on day-to-day KPIs. Export the edited table above to share"
        " with production, quality, and leadership teams."
    )


if __name__ == "__main__":
    main()
