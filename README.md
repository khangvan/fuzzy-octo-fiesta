# Scheduling Optimizer Demo

This repository contains a lightweight multi-page [Streamlit](https://streamlit.io/) application for
experimenting with task scheduling scenarios and tracking production KPIs.

## Application structure

- **`app.py` – Scheduling Optimizer**
  - Enter backlog items (name, hours, optional due date) and specify the number of hours you can dedicate
    each day. The app sorts tasks by due date and produces a simple multi-day schedule so you can spot
    overloaded days quickly.
- **`pages/1_Scheduling_Optimizing.py` – Scheduling insights**
  - Highlights common optimization goals and includes a what-if calculator showing how effort, capacity,
    and task count impact the delivery timeline.
- **`pages/2_KPI_Production_Report.py` – KPI Production Report**
  - Capture line/shift performance data, compute derived KPIs (variance, attainment, scrap, downtime),
    and visualize output versus target in a chart for quick reporting.

## Getting started

1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install streamlit pandas
   ```
2. Launch the Streamlit app from the repository root:
   ```bash
   streamlit run app.py
   ```
3. Use the sidebar in the main app to configure available hours and open the additional pages from the
   Streamlit page selector.

## Repository layout

```
.
├── app.py                     # Main scheduling optimizer entry point
├── pages
│   ├── 1_Scheduling_Optimizing.py
│   └── 2_KPI_Production_Report.py
└── README.md
```
