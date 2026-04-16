
import os
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# CONFIG
# =========================
DATA_FILE = "hospital_operations_dataset_2025.csv"
OUTPUT_DIR = "outputs"

# =========================
# LOAD
# =========================
if not os.path.exists(DATA_FILE):
    raise FileNotFoundError(
        f"Arquivo não encontrado: {DATA_FILE}\n"
        "Coloque o CSV na mesma pasta do analysis.py ou ajuste a variável DATA_FILE."
    )

os.makedirs(OUTPUT_DIR, exist_ok=True)

df = pd.read_csv(DATA_FILE)

# =========================
# CLEANING / TYPES
# =========================
df["triage_time"] = pd.to_datetime(df["triage_time"], errors="coerce")
df["date"] = pd.to_datetime(df["date"], errors="coerce")

numeric_cols = [
    "record_id",
    "hour",
    "month",
    "prescriptions_count",
    "pharmacists_on_shift",
    "triage_time_minutes",
    "triage_sla_minutes",
    "delay_flag",
    "on_time_flag",
    "analysis_completed_flag",
    "delivery_time_minutes",
    "delivery_delay_flag",
]

for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# remove linhas sem dados essenciais
df = df.dropna(subset=["triage_time", "department", "triage_time_minutes"]).copy()

# colunas derivadas
df["hour_from_datetime"] = df["triage_time"].dt.hour
df["triage_delay_minutes"] = df["triage_time_minutes"] - df["triage_sla_minutes"]
df["triage_delay_minutes"] = df["triage_delay_minutes"].clip(lower=0)
df["delivery_vs_triage_gap"] = df["delivery_time_minutes"] - df["triage_time_minutes"]

# =========================
# OVERVIEW
# =========================
print("=" * 60)
print("HOSPITAL OPERATIONS ANALYSIS")
print("=" * 60)
print(f"Rows: {len(df):,}")
print(f"Period: {df['triage_time'].min()} to {df['triage_time'].max()}")
print(f"Departments: {df['department'].nunique()}")
print(f"Pharmacy units: {df['pharmacy_unit'].nunique()}")
print("=" * 60)

delay_rate = df["delay_flag"].mean() * 100
delivery_delay_rate = df["delivery_delay_flag"].mean() * 100
analysis_completion_rate = df["analysis_completed_flag"].mean() * 100
avg_triage = df["triage_time_minutes"].mean()
avg_delivery = df["delivery_time_minutes"].mean()

print(f"Average triage time: {avg_triage:.2f} minutes")
print(f"Average delivery time: {avg_delivery:.2f} minutes")
print(f"Triage delay rate: {delay_rate:.2f}%")
print(f"Delivery delay rate: {delivery_delay_rate:.2f}%")
print(f"Analysis completion rate: {analysis_completion_rate:.2f}%")
print("=" * 60)

# =========================
# TABLES
# =========================
dept_summary = (
    df.groupby("department")
    .agg(
        records=("record_id", "count"),
        avg_triage_time=("triage_time_minutes", "mean"),
        avg_delivery_time=("delivery_time_minutes", "mean"),
        delay_rate=("delay_flag", "mean"),
        delivery_delay_rate=("delivery_delay_flag", "mean"),
        avg_prescriptions=("prescriptions_count", "mean"),
        avg_staff=("pharmacists_on_shift", "mean"),
    )
    .sort_values("delay_rate", ascending=False)
)

dept_summary["delay_rate"] *= 100
dept_summary["delivery_delay_rate"] *= 100

hour_summary = (
    df.groupby("hour_from_datetime")
    .agg(
        records=("record_id", "count"),
        avg_triage_time=("triage_time_minutes", "mean"),
        delay_rate=("delay_flag", "mean"),
        avg_prescriptions=("prescriptions_count", "mean"),
    )
    .sort_values("hour_from_datetime")
)

hour_summary["delay_rate"] *= 100

shift_summary = (
    df.groupby("shift")
    .agg(
        records=("record_id", "count"),
        avg_triage_time=("triage_time_minutes", "mean"),
        delay_rate=("delay_flag", "mean"),
        avg_delivery_time=("delivery_time_minutes", "mean"),
    )
    .sort_values("delay_rate", ascending=False)
)

shift_summary["delay_rate"] *= 100

weekday_summary = (
    df.groupby("weekday")
    .agg(
        records=("record_id", "count"),
        avg_triage_time=("triage_time_minutes", "mean"),
        delay_rate=("delay_flag", "mean"),
    )
)

weekday_summary["delay_rate"] *= 100

priority_summary = (
    df.groupby("priority")
    .agg(
        records=("record_id", "count"),
        avg_triage_time=("triage_time_minutes", "mean"),
        delay_rate=("delay_flag", "mean"),
    )
    .sort_values("avg_triage_time", ascending=False)
)

priority_summary["delay_rate"] *= 100

# save tables
dept_summary.round(2).to_csv(os.path.join(OUTPUT_DIR, "department_summary.csv"))
hour_summary.round(2).to_csv(os.path.join(OUTPUT_DIR, "hour_summary.csv"))
shift_summary.round(2).to_csv(os.path.join(OUTPUT_DIR, "shift_summary.csv"))
weekday_summary.round(2).to_csv(os.path.join(OUTPUT_DIR, "weekday_summary.csv"))
priority_summary.round(2).to_csv(os.path.join(OUTPUT_DIR, "priority_summary.csv"))

print("\nTop 5 departments by triage delay rate:")
print(dept_summary[["records", "avg_triage_time", "delay_rate"]].head().round(2))

print("\nHourly summary:")
print(hour_summary[["records", "avg_triage_time", "delay_rate"]].round(2))

print("\nShift summary:")
print(shift_summary.round(2))

# =========================
# INSIGHTS
# =========================
worst_hour = hour_summary["delay_rate"].idxmax()
worst_department = dept_summary["delay_rate"].idxmax()
worst_shift = shift_summary["delay_rate"].idxmax()

corr_prescriptions_triage = df["prescriptions_count"].corr(df["triage_time_minutes"])
corr_staff_triage = df["pharmacists_on_shift"].corr(df["triage_time_minutes"])

print("\n" + "=" * 60)
print("AUTOMATED INSIGHTS")
print("=" * 60)
print(f"Worst hour for delays: {worst_hour}:00 ({hour_summary.loc[worst_hour, 'delay_rate']:.2f}% delayed)")
print(f"Worst department for delays: {worst_department} ({dept_summary.loc[worst_department, 'delay_rate']:.2f}% delayed)")
print(f"Worst shift for delays: {worst_shift} ({shift_summary.loc[worst_shift, 'delay_rate']:.2f}% delayed)")
print(f"Correlation: prescriptions_count vs triage_time_minutes = {corr_prescriptions_triage:.2f}")
print(f"Correlation: pharmacists_on_shift vs triage_time_minutes = {corr_staff_triage:.2f}")

# =========================
# CHARTS
# =========================

# 1. Average triage time by hour
plt.figure(figsize=(10, 5))
hour_summary["avg_triage_time"].plot(marker="o")
plt.title("Average Triage Time by Hour")
plt.xlabel("Hour")
plt.ylabel("Minutes")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "avg_triage_time_by_hour.png"), dpi=300)
plt.close()

# 2. Delay rate by department
plt.figure(figsize=(11, 6))
dept_summary["delay_rate"].sort_values().plot(kind="barh")
plt.title("Triage Delay Rate by Department")
plt.xlabel("Delay Rate (%)")
plt.ylabel("Department")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "triage_delay_rate_by_department.png"), dpi=300)
plt.close()

# 3. Prescriptions vs triage time
plt.figure(figsize=(8, 6))
plt.scatter(df["prescriptions_count"], df["triage_time_minutes"], alpha=0.25)
plt.title("Prescriptions Count vs Triage Time")
plt.xlabel("Prescriptions Count")
plt.ylabel("Triage Time (minutes)")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "prescriptions_vs_triage_time.png"), dpi=300)
plt.close()

# 4. Avg triage time by shift
plt.figure(figsize=(8, 5))
shift_summary["avg_triage_time"].sort_values(ascending=False).plot(kind="bar")
plt.title("Average Triage Time by Shift")
plt.xlabel("Shift")
plt.ylabel("Minutes")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "avg_triage_time_by_shift.png"), dpi=300)
plt.close()

# 5. Delivery delay rate by department
plt.figure(figsize=(11, 6))
dept_summary["delivery_delay_rate"].sort_values().plot(kind="barh")
plt.title("Delivery Delay Rate by Department")
plt.xlabel("Delivery Delay Rate (%)")
plt.ylabel("Department")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "delivery_delay_rate_by_department.png"), dpi=300)
plt.close()

# 6. Monthly volume
monthly_volume = df.groupby("month")["record_id"].count()
plt.figure(figsize=(10, 5))
monthly_volume.plot(marker="o")
plt.title("Monthly Volume of Records")
plt.xlabel("Month")
plt.ylabel("Records")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "monthly_volume.png"), dpi=300)
plt.close()

print("\nArquivos salvos em:", OUTPUT_DIR)
print("- department_summary.csv")
print("- hour_summary.csv")
print("- shift_summary.csv")
print("- weekday_summary.csv")
print("- priority_summary.csv")
print("- avg_triage_time_by_hour.png")
print("- triage_delay_rate_by_department.png")
print("- prescriptions_vs_triage_time.png")
print("- avg_triage_time_by_shift.png")
print("- delivery_delay_rate_by_department.png")
print("- monthly_volume.png")
