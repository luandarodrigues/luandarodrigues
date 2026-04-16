# Prescription Data – SQL Analysis

## Overview

This project analyzes prescription workflow data using SQL to identify operational bottlenecks, delay patterns, and department-level differences in hospital pharmacy activity.

The goal is to show how structured queries can support operational decision-making, especially in high-volume healthcare environments.

## Business Question

Which departments and operational conditions are associated with higher prescription-related delays, and how can SQL be used to monitor these patterns?

## Analysis Goals

- measure prescription volume by department
- compare average triage time across departments
- identify where delays are most concentrated
- evaluate performance by shift and priority
- connect workload patterns to operational performance

## Key Questions

1. Which departments have the highest average delays?
2. Which shifts concentrate the largest workload?
3. How does prescription volume relate to triage performance?
4. Which priority groups show the highest delay rate?
5. Which monthly or weekday patterns deserve attention?

## Files in This Project

- [`queries.sql`](./queries.sql) – main SQL queries
- [`query_explanations.md`](./query_explanations.md) – explanation of business logic behind each query
- [`schema_reference.md`](./schema_reference.md) – expected table structure and key fields
- [`sample_results_template.md`](./sample_results_template.md) – template to paste results or screenshots
- [`data/README.md`](./data/README.md) – source data guidance

## Recommended Deliverables

This project is intended to include:

- SQL query set
- result screenshots or exported tables
- short interpretation of findings

## Tools

- SQL
- CSV / relational table structure
- hospital operations logic

## Notes

The analysis can reuse the dataset from the `hospital-operations` project after import into a SQL environment such as SQLite, PostgreSQL, MySQL, or SQL Server.
