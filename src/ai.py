import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def generate_ai_insight(df):

    anomalies = df[df["is_anomaly"] == 1]

    if anomalies.empty:
        return "No significant business anomalies were detected."

    # Highest-impact anomaly
    top_anomaly = anomalies.sort_values(
        "impact_score",
        ascending=False
    ).iloc[0]

    region = top_anomaly["region"]
    category = top_anomaly["category"]
    product = top_anomaly["product"]
    revenue = top_anomaly["revenue"]
    impact = top_anomaly["impact_score"]

    # Region analysis
    region_anomalies = anomalies[
        anomalies["region"] == region
    ]

    region_count = len(region_anomalies)
    region_revenue = region_anomalies["revenue"].sum()

    # Category analysis
    category_anomalies = anomalies[
        anomalies["category"] == category
    ]

    category_count = len(category_anomalies)
    category_revenue = category_anomalies["revenue"].sum()

    fallback = (
        f"KPIX detected a significant business anomaly involving "
        f"{product} in the {category} category in the {region} region. "
        f"The highest-impact transaction generated revenue of "
        f"{revenue:.2f}. The {region} region contains "
        f"{region_count} detected anomalies with combined anomaly "
        f"revenue of {region_revenue:.2f}. The {category} category "
        f"contains {category_count} detected anomalies with combined "
        f"anomaly revenue of {category_revenue:.2f}. "
        f"This pattern should be investigated further to determine "
        f"whether it is related to unusual demand, pricing, quantity, "
        f"or data quality."
    )

    prompt = f"""
You are KPIX, an AI business intelligence assistant.

Analyze this business anomaly data.

Product: {product}
Category: {category}
Region: {region}

Highest-impact transaction revenue: {revenue:.2f}
Impact score: {impact:.2f}

Region:
- Anomaly count: {region_count}
- Combined anomaly revenue: {region_revenue:.2f}

Category:
- Anomaly count: {category_count}
- Combined anomaly revenue: {category_revenue:.2f}

Write a concise business insight in 3 to 5 sentences.

The response MUST:
1. Explain what the data shows.
2. Mention the important region/category/product involved.
3. Mention the financial impact using the revenue values.
4. Explain that the exact cause is not known.
5. Suggest what the business should investigate.

Do not simply repeat the numbers.
Do not invent facts.
Do not make up a cause.
Do not mention the impact score unless it helps explain the finding.
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        return response.text

    except Exception:
        return fallback