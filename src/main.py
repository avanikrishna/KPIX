from recommendation import generate_recommendation
from ai import generate_ai_insight
from investigation import create_incident_cards
from investigation import calculate_impact_score
from investigation import investigate_anomalies
from database import load_sales_data
from kpi import calculate_kpis
from anomaly import detect_anomalies
from ask_kpix import ask_kpix

# Load data
df = load_sales_data()

# Calculate KPIs
kpis = calculate_kpis(df)

print("\n===== KPIX BUSINESS KPIs =====")
print("Total Sales:", kpis["total_sales"])
print("Total Revenue:", round(kpis["total_revenue"], 2))
print("Average Sale:", round(kpis["average_sale"], 2))
print("Total Quantity:", kpis["total_quantity"])
print("Unique Customers:", kpis["unique_customers"])

# Detect anomalies
df = detect_anomalies(df)
df = calculate_impact_score(df)

anomaly_count = df["is_anomaly"].sum()

print("\n===== KPIX ANOMALY DETECTION =====")
print("Anomalies detected:", anomaly_count)

# Display top anomalies
print("\n===== TOP ANOMALIES =====")

anomalies = df[df["is_anomaly"] == 1]

print(
    anomalies[
        ["id", "sale_date", "region", "category",
         "product", "quantity", "unit_price", "revenue"]
    ]
    .sort_values("revenue", ascending=False)
    .head(10)
)
# Investigate anomalies
region_analysis, category_analysis, product_analysis, driver_analysis = investigate_anomalies(df)

print("\n===== ANOMALY INVESTIGATION: REGION =====")
print(region_analysis)

print("\n===== ANOMALY INVESTIGATION: CATEGORY =====")
print(category_analysis)

print("\n===== ANOMALY INVESTIGATION: PRODUCT =====")
print(product_analysis)

print("\n===== BUSINESS DRIVER ANALYSIS =====")
print(driver_analysis.head(10))

print("\n===== HIGH IMPACT ANOMALIES =====")

high_impact = (
    df[df["is_anomaly"] == 1]
    .sort_values("impact_score", ascending=False)
    .head(10)
)

print(
    high_impact[
        ["id", "region", "category", "product",
         "revenue", "impact_score"]
    ]
)
# Create incident cards
incidents = create_incident_cards(df)

print("\n===== KPIX BUSINESS INCIDENT CARDS =====")
print(incidents.to_string(index=False))
# Generate AI insight
ai_insight = generate_ai_insight(df)

print("\n===== KPIX AI BUSINESS INSIGHT =====")
print(ai_insight)
# Generate business recommendation
recommendation = generate_recommendation(df)

print("\n===== KPIX BUSINESS RECOMMENDATION =====")
print(recommendation)
# Export incident cards for Power BI
incidents.to_csv(
    "output/incident_cards.csv",
    index=False
)

print("\nIncident cards exported successfully.")
# Export incident cards for Power BI
incidents.to_csv(
    "output/incident_cards.csv",
    index=False
)

print("\nIncident cards exported successfully.")
# Export complete KPIX analysis data
df.to_csv(
    "output/kpix_analysis.csv",
    index=False
)

print("KPIX analysis data exported successfully.")
print("\n===== ASK KPIX =====")

question = input("Ask KPIX a question: ")

answer = ask_kpix(df, question)

print("KPIX:", answer)
