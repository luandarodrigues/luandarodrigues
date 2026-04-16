-- 1. Average triage time and delay rate by department
SELECT 
    department,
    COUNT(*) AS total_records,
    AVG(triage_time_minutes) AS avg_triage_time,
    SUM(delay_flag) * 1.0 / COUNT(*) AS delay_rate
FROM data
GROUP BY department
ORDER BY delay_rate DESC;

-- 2. Workload by shift
SELECT 
    shift,
    COUNT(*) AS total_records,
    AVG(triage_time_minutes) AS avg_triage_time
FROM data
GROUP BY shift
ORDER BY total_records DESC;

-- 3. Hourly delay pattern
SELECT 
    EXTRACT(HOUR FROM triage_time) AS hour,
    COUNT(*) AS total_records,
    AVG(triage_time_minutes) AS avg_triage_time,
    SUM(delay_flag) * 1.0 / COUNT(*) AS delay_rate
FROM data
GROUP BY hour
ORDER BY hour;

-- 4. Workload vs performance
SELECT 
    prescriptions_count,
    AVG(triage_time_minutes) AS avg_triage_time
FROM data
GROUP BY prescriptions_count
ORDER BY prescriptions_count;

-- 5. Priority impact
SELECT 
    priority,
    COUNT(*) AS total_records,
    AVG(triage_time_minutes) AS avg_triage_time,
    SUM(delay_flag) * 1.0 / COUNT(*) AS delay_rate
FROM data
GROUP BY priority
ORDER BY delay_rate DESC;

-- 6. Monthly trend
SELECT 
    DATE_TRUNC('month', triage_time) AS month,
    COUNT(*) AS total_records
FROM data
GROUP BY month
ORDER BY month;
