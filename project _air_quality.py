# Nainika Singh ṇ
# 2026B01010340
# git -https://github.com/NainikaSingh0340/AIR-QUALITY-INSIGHTS-DASHBOARD
import pandas as pd
import numpy as np

df = pd.read_csv("04_air_quality.csv")
print(df.shape)
print(df.dtypes)
print(df.isnull().sum())

df["PM25"] = df["PM25"].fillna(df["PM25"].median())
df["Date"] = pd.to_datetime(df["Date"])
df["Month"] = df["Date"].dt.month_name()

print("\nAverage pollution by city")
print(df.groupby("City")[["PM25", "PM10", "NO2"]].mean().round(2))

worst_city = df.groupby("City")["PM25"].mean().idxmax()
best_city = df.groupby("City")["PM25"].mean().idxmin()
print("\nMost polluted city:", worst_city)
print("Cleanest city:", best_city)

def aqi_level(pm25):
    if pm25 <= 30:
        return "Good"
    elif pm25 <= 60:
        return "Moderate"
    elif pm25 <= 90:
        return "Poor"
    return "Very Poor"

df["Level"] = df["PM25"].apply(aqi_level)
print("\nDays in each level")
print(df["Level"].value_counts())

monthly = df.groupby("Month")["PM25"].mean().round(2)
print("\nWorst month:", monthly.idxmax(), monthly.max())
print("Best month:", monthly.idxmin(), monthly.min())

print("\nCorrelation with PM25")
print(df[["PM25", "PM10", "NO2", "Temperature_C", "Humidity_Percent"]].corr()["PM25"].round(2))

q1 = np.percentile(df["PM25"], 25)
q3 = np.percentile(df["PM25"], 75)
upper = q3 + 1.5 * (q3 - q1)
print("\nPM2.5 outliers:", (df["PM25"] > upper).sum())
print("Temperature above 50C (likely errors):", (df["Temperature_C"] > 50).sum())

df.to_csv("04_air_quality_cleaned.csv", index=False)