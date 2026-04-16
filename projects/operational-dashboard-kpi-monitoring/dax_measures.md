# DAX Measures

## Core KPIs

```DAX
Avg Triage Time = AVERAGE(data[triage_time_minutes])

Avg Delivery Time = AVERAGE(data[delivery_time_minutes])

Triage Delay Rate = DIVIDE(SUM(data[delay_flag]), COUNT(data[delay_flag]))

Delivery Delay Rate = DIVIDE(SUM(data[delivery_delay_flag]), COUNT(data[delivery_delay_flag]))

Completion Rate = DIVIDE(SUM(data[analysis_completed_flag]), COUNT(data[analysis_completed_flag]))
```

## Supporting Columns

```DAX
Hour = HOUR(data[triage_time])
Month = FORMAT(data[triage_time], "MMM")
Weekday = FORMAT(data[triage_time], "dddd")
```
