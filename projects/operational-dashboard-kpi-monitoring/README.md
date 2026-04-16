# Operational Dashboard – KPI Monitoring

## Overview

This project defines an operational dashboard for hospital pharmacy KPI monitoring, focused on response time, SLA adherence, workload pressure, and department-level performance.

The dashboard is designed for management use. Its goal is not only to display metrics, but to support quick operational decisions around delays, bottlenecks, and resource allocation.

## Business Question

How can hospital pharmacy operations be monitored in a way that makes delays visible early, highlights critical departments, and supports faster management action?

## Dashboard Goal

Provide a clear view of:

- where delays are happening
- when delays concentrate
- whether workload or staffing is driving performance loss
- which departments require immediate attention

## Core KPIs

- **Average Triage Time**
- **Average Delivery Time**
- **Triage Delay Rate**
- **Delivery Delay Rate**
- **Analysis Completion Rate**

## Recommended Layout

### Top row – KPI cards
- Average Triage Time
- Average Delivery Time
- Triage Delay Rate
- Delivery Delay Rate
- Completion Rate

### Middle row – Time and bottleneck analysis
- Triage Time by Hour
- Delay Rate by Hour
- Triage Time by Shift
- Delay Rate by Department

### Bottom row – Operational drivers
- Prescriptions vs Triage Time
- Delivery Delay by Department
- Monthly Volume Trend

## Suggested Filters

- Department
- Shift
- Priority
- Month
- Pharmacy Unit

## Main Insights Expected

Based on the underlying operational analysis, the dashboard should make three points immediately visible:

1. Delays concentrate in the **afternoon shift**
2. **Pronto Socorro** is a critical outlier
3. **Workload volume** has stronger impact on delay than staffing levels alone

## Files in This Project

- [`dax_measures.md`](./dax_measures.md) – DAX measures for Power BI
- [`kpi_definitions.csv`](./kpi_definitions.csv) – KPI catalog and formulas
- [`dashboard_wireframe.md`](./dashboard_wireframe.md) – suggested layout and design logic
- [`screenshots/README.md`](./screenshots/README.md) – where dashboard images should be stored
- [`data/README.md`](./data/README.md) – source data guidance

## Recommended Output

This project is intended to result in:

- a `.pbix` dashboard file
- screenshots for GitHub display
- a recruiter-friendly summary of operational insights

## Tools

- Power BI
- DAX
- Python / CSV as upstream data preparation

## Notes

The source dataset can be reused from the `hospital-operations` project or refreshed with new operational extracts.
