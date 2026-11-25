from flask import Flask, render_template, request
import sys
import os
import subprocess

app = Flask(__name__)

# Add src folder to Python path
sys.path.append(
    os.path.join(os.path.dirname(__file__), "..", "src")
)

from database import load_sales_data
from kpi import calculate_kpis
from anomaly import detect_anomalies
from investigation import (
    calculate_impact_score,
    create_incident_cards
)
from ai import generate_ai_insight
from recommendation import generate_recommendation
from ask_kpix import ask_kpix


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate-data", methods=["POST"])
def generate_data():

    # Generate new sales dataset
    subprocess.run(
        ["python", "src/generate_data.py"],
        check=True
    )

    # Load generated dataset into MySQL
    subprocess.run(
        ["python", "src/load_generated_data.py"],
        check=True
    )

    return render_template(
        "index.html",
        data_generated=True
    )


@app.route("/analyze", methods=["POST"])
def analyze():

    # Load sales data
    df = load_sales_data()

    # Calculate KPIs
    kpis = calculate_kpis(df)

    # Detect anomalies
    df = detect_anomalies(df)

    # Calculate impact score
    df = calculate_impact_score(df)

    # Create business incident cards
    incidents_df = create_incident_cards(df)
    incidents = incidents_df.head(10).to_dict("records")

    # Count anomalies
    anomaly_count = int(df["is_anomaly"].sum())

    # Get top anomalies
    top_anomalies = (
        df[df["is_anomaly"] == 1]
        .sort_values("revenue", ascending=False)
        .head(10)
    )

    anomalies = top_anomalies.to_dict("records")

    # Revenue by region
    revenue_by_region = (
        df.groupby("region")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    region_labels = revenue_by_region.index.tolist()
    region_values = revenue_by_region.values.tolist()

    # Anomalies by category
    anomalies_by_category = (
        df[df["is_anomaly"] == 1]
        .groupby("category")
        .size()
        .sort_values(ascending=False)
    )

    category_labels = anomalies_by_category.index.tolist()
    category_values = anomalies_by_category.values.tolist()

    # Anomaly revenue by product
    anomaly_revenue_by_product = (
        df[df["is_anomaly"] == 1]
        .groupby("product")["revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(8)
    )

    product_labels = anomaly_revenue_by_product.index.tolist()
    product_values = anomaly_revenue_by_product.values.tolist()

    # Generate AI insight
    ai_insight = generate_ai_insight(df)

    # Generate business recommendation
    recommendation = generate_recommendation(df)

    # Render dashboard
    return render_template(
        "index.html",
        kpis=kpis,
        anomaly_count=anomaly_count,
        anomalies=anomalies,
        incidents=incidents,
        ai_insight=ai_insight,
        recommendation=recommendation,
        region_labels=region_labels,
        region_values=region_values,
        category_labels=category_labels,
        category_values=category_values,
        product_labels=product_labels,
        product_values=product_values,
        analyzed=True
    )


@app.route("/ask-kpix", methods=["POST"])
def ask_kpix_route():

    # Get user's question
    question = request.form["question"]

    # Load sales data
    df = load_sales_data()

    # Calculate KPIs
    kpis = calculate_kpis(df)

    # Detect anomalies
    df = detect_anomalies(df)

    # Calculate impact score
    df = calculate_impact_score(df)

    # Create business incident cards
    incidents_df = create_incident_cards(df)
    incidents = incidents_df.head(10).to_dict("records")

    # Count anomalies
    anomaly_count = int(df["is_anomaly"].sum())

    # Get top anomalies
    top_anomalies = (
        df[df["is_anomaly"] == 1]
        .sort_values("revenue", ascending=False)
        .head(10)
    )

    anomalies = top_anomalies.to_dict("records")

    # Revenue by region
    revenue_by_region = (
        df.groupby("region")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    region_labels = revenue_by_region.index.tolist()
    region_values = revenue_by_region.values.tolist()

    # Anomalies by category
    anomalies_by_category = (
        df[df["is_anomaly"] == 1]
        .groupby("category")
        .size()
        .sort_values(ascending=False)
    )

    category_labels = anomalies_by_category.index.tolist()
    category_values = anomalies_by_category.values.tolist()

    # Anomaly revenue by product
    anomaly_revenue_by_product = (
        df[df["is_anomaly"] == 1]
        .groupby("product")["revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(8)
    )

    product_labels = anomaly_revenue_by_product.index.tolist()
    product_values = anomaly_revenue_by_product.values.tolist()

    # Generate AI insight
    ai_insight = generate_ai_insight(df)

    # Generate business recommendation
    recommendation = generate_recommendation(df)

    # Ask KPIX
    answer = ask_kpix(df, question)

    # Render the FULL dashboard with the answer
    return render_template(
        "index.html",
        kpis=kpis,
        anomaly_count=anomaly_count,
        anomalies=anomalies,
        incidents=incidents,
        ai_insight=ai_insight,
        recommendation=recommendation,
        region_labels=region_labels,
        region_values=region_values,
        category_labels=category_labels,
        category_values=category_values,
        product_labels=product_labels,
        product_values=product_values,
        question=question,
        answer=answer,
        analyzed=True
    )


if __name__ == "__main__":
    app.run(debug=True)