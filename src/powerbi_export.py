from database import load_sales_data
from anomaly import detect_anomalies
from investigation import calculate_impact_score


# Load business data
df = load_sales_data()

# Detect anomalies
df = detect_anomalies(df)

# Calculate business impact
df = calculate_impact_score(df)

# Export Power BI dataset
df.to_csv(
    "output/kpix_powerbi_data.csv",
    index=False
)

print("KPIX Power BI dataset exported successfully.")
print(f"Rows exported: {len(df)}")
print(f"Columns exported: {len(df.columns)}")
