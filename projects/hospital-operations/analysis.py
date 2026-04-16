import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("data.csv")

# Convert datetime
df['triage_time'] = pd.to_datetime(df['triage_time'])

# Extract hour
df['hour'] = df['triage_time'].dt.hour

# --- Analysis 1: Average triage time by hour ---
avg_time = df.groupby('hour')['triage_time_minutes'].mean()

plt.figure()
avg_time.plot()
plt.title("Average Triage Time by Hour")
plt.xlabel("Hour")
plt.ylabel("Minutes")
plt.show()

# --- Analysis 2: Delay rate ---
delay_rate = df['delay_flag'].mean() * 100
print(f"Delay Rate: {delay_rate:.2f}%")

# --- Analysis 3: Department performance ---
dept_analysis = df.groupby('department')['triage_time_minutes'].mean()
print(dept_analysis)

# --- Analysis 4: Prescriptions vs time ---
plt.figure()
plt.scatter(df['prescriptions_count'], df['triage_time_minutes'])
plt.title("Prescriptions vs Triage Time")
plt.xlabel("Prescriptions")
plt.ylabel("Minutes")
plt.show()
