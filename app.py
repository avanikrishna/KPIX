import streamlit as st
import sys
import os

# Allow app.py to access files inside src/
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from database import load_sales_data
from kpi import calculate_kpis
from anomaly import detect_anomalies
from investigation import (
    calculate_impact_score,
    investigate_anomalies,
    create_incident_cards
)


st.set_page_config(
    page_title="KPIX",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# LOAD KPIX DATA
# -----------------------------

df = load_sales_data()

kpis = calculate_kpis(df)

df = detect_anomalies(df)

df = calculate_impact_score(df)


# -----------------------------
# SIDEBAR
# -----------------------------

st.sidebar.title("KPIX")

page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "Anomaly Investigation",
        "Incident Monitor",
        "AI Insights",
        "Recommendations",
        "Ask KPIX"
    ]
)


# -----------------------------
# OVERVIEW
# -----------------------------

if page == "Overview":

    st.title("KPIX — AI-Powered Business Intelligence")

    st.write(
        "Detect → Investigate → Measure Impact → Explain → Recommend"
    )

    st.divider()

    st.subheader("Business Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Sales",
            f"{kpis['total_sales']:,}"
        )

    with col2:
        st.metric(
            "Total Revenue",
            f"₹{kpis['total_revenue']:,.2f}"
        )

    with col3:
        anomaly_count = df["is_anomaly"].sum()

        st.metric(
            "Anomalies",
            f"{anomaly_count:,}"
        )

    with col4:
        st.metric(
            "Customers",
            f"{kpis['unique_customers']:,}"
        )

    st.divider()

    # Revenue by Region

    st.subheader("Revenue by Region")

    region_revenue = (
        df.groupby("region")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(region_revenue)

    st.divider()

    # High Impact Incidents

    st.subheader("High-Impact Business Incidents")

    high_impact = (
        df[df["is_anomaly"] == 1]
        .sort_values(
            "impact_score",
            ascending=False
        )
        .copy()
    )

    high_impact["severity"] = high_impact[
        "impact_score"
    ].apply(
        lambda x:
        "HIGH" if x >= 75
        else "MEDIUM" if x >= 50
        else "LOW"
    )

    st.dataframe(
        high_impact[
            [
                "id",
                "sale_date",
                "region",
                "category",
                "product",
                "revenue",
                "impact_score",
                "severity"
            ]
        ].head(10),
        use_container_width=True
    )


# -----------------------------
# OTHER PAGES
# -----------------------------

elif page == "Anomaly Investigation":

    st.title("🔎 Anomaly Investigation")

    st.write(
        "KPIX investigates detected anomalies across region, "
        "category, product, and business drivers."
    )

    region_analysis, category_analysis, product_analysis, driver_analysis = (
        investigate_anomalies(df)
    )

    st.subheader("Anomalies by Region")

    st.dataframe(
        region_analysis,
        use_container_width=True
    )

    st.subheader("Anomalies by Category")

    st.dataframe(
        category_analysis,
        use_container_width=True
    )

    st.subheader("Anomalies by Product")

    st.dataframe(
        product_analysis,
        use_container_width=True
    )

    st.subheader("Top Business Drivers")

    st.dataframe(
        driver_analysis.head(10),
        use_container_width=True
    )


elif page == "Incident Monitor":

    st.title("🚨 Incident Monitor")

    st.write(
        "KPIX prioritizes unusual business transactions "
        "using impact score and severity."
    )

    incident_cards = create_incident_cards(df)

    st.subheader("Business Incident Cards")

    st.dataframe(
        incident_cards,
        use_container_width=True
    )

elif page == "AI Insights":

    st.title("🤖 AI Insights")

    st.info(
        "This page will contain AI-generated business explanations."
    )


elif page == "Recommendations":

    st.title("💡 Recommendations")

    st.info(
        "This page will contain KPIX business recommendations."
    )


elif page == "Ask KPIX":

    st.title("💬 Ask KPIX")

    st.info(
        "This page will contain the KPIX question-answering assistant."
    )