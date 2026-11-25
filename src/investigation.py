import pandas as pd


def investigate_anomalies(df):

    anomalies = df[df["is_anomaly"] == 1]

    # ----------------------------------------------------------
    # REGION ANALYSIS
    # ----------------------------------------------------------

    region_analysis = (
        anomalies.groupby("region")
        .agg(
            anomaly_count=("id", "count"),
            anomaly_revenue=("revenue", "sum")
        )
        .sort_values(
            "anomaly_revenue",
            ascending=False
        )
    )

    # ----------------------------------------------------------
    # CATEGORY ANALYSIS
    # ----------------------------------------------------------

    category_analysis = (
        anomalies.groupby("category")
        .agg(
            anomaly_count=("id", "count"),
            anomaly_revenue=("revenue", "sum")
        )
        .sort_values(
            "anomaly_revenue",
            ascending=False
        )
    )

    # ----------------------------------------------------------
    # PRODUCT ANALYSIS
    # ----------------------------------------------------------

    product_analysis = (
        anomalies.groupby("product")
        .agg(
            anomaly_count=("id", "count"),
            anomaly_revenue=("revenue", "sum")
        )
        .sort_values(
            "anomaly_revenue",
            ascending=False
        )
    )

    # ----------------------------------------------------------
    # BUSINESS DRIVER ANALYSIS
    # ----------------------------------------------------------

    driver_analysis = (
        anomalies.groupby(
            ["region", "category", "product"]
        )
        .agg(
            anomaly_count=("id", "count"),
            anomaly_revenue=("revenue", "sum")
        )
        .sort_values(
            "anomaly_revenue",
            ascending=False
        )
    )

    return (
        region_analysis,
        category_analysis,
        product_analysis,
        driver_analysis
    )


def calculate_impact_score(df):

    anomalies = df["is_anomaly"] == 1

    # ----------------------------------------------------------
    # REVENUE SCORE
    # ----------------------------------------------------------

    max_revenue = df.loc[
        anomalies,
        "revenue"
    ].max()

    if max_revenue > 0:

        revenue_score = (
            df["revenue"] / max_revenue
        ) * 100

    else:

        revenue_score = 0

    # ----------------------------------------------------------
    # ANOMALY STRENGTH SCORE
    # ----------------------------------------------------------

    max_strength = df.loc[
        anomalies,
        "anomaly_strength"
    ].max()

    if max_strength > 0:

        anomaly_strength_score = (
            df["anomaly_strength"] / max_strength
        ) * 100

    else:

        anomaly_strength_score = 0

    # ----------------------------------------------------------
    # BUSINESS DRIVER FREQUENCY SCORE
    # ----------------------------------------------------------

    driver_counts = (
        df.groupby(
            ["region", "category", "product"]
        )["id"]
        .transform("count")
    )

    max_driver_count = driver_counts[
        anomalies
    ].max()

    if max_driver_count > 0:

        driver_score = (
            driver_counts / max_driver_count
        ) * 100

    else:

        driver_score = 0

    # ----------------------------------------------------------
    # FINAL IMPACT SCORE
    # ----------------------------------------------------------

    df["impact_score"] = (
        (revenue_score * 0.40)
        +
        (anomaly_strength_score * 0.40)
        +
        (driver_score * 0.20)
    ).clip(
        0,
        100
    ).round(2)

    return df


def create_incident_cards(df):

    # ----------------------------------------------------------
    # GET ALL ANOMALIES
    # ----------------------------------------------------------

    anomalies = (
        df[df["is_anomaly"] == 1]
        .copy()
    )

    if anomalies.empty:

        return pd.DataFrame(
            columns=[
                "id",
                "sale_date",
                "region",
                "category",
                "product",
                "revenue",
                "impact_score",
                "severity"
            ]
        )

    # ----------------------------------------------------------
    # ASSIGN SEVERITY
    # ----------------------------------------------------------

    anomalies["severity"] = anomalies[
        "impact_score"
    ].apply(
        lambda x:
        "HIGH"
        if x >= 80
        else "MEDIUM"
        if x >= 50
        else "LOW"
    )

    # ----------------------------------------------------------
    # SELECT HIGH-IMPACT INCIDENTS
    # ----------------------------------------------------------

    high = (
        anomalies[
            anomalies["severity"] == "HIGH"
        ]
        .sort_values(
            "impact_score",
            ascending=False
        )
        .head(4)
    )

    # ----------------------------------------------------------
    # SELECT MEDIUM-IMPACT INCIDENTS
    # ----------------------------------------------------------

    medium = (
        anomalies[
            anomalies["severity"] == "MEDIUM"
        ]
        .sort_values(
            "impact_score",
            ascending=False
        )
        .head(3)
    )

    # ----------------------------------------------------------
    # SELECT LOW-IMPACT INCIDENTS
    # ----------------------------------------------------------

    low = (
        anomalies[
            anomalies["severity"] == "LOW"
        ]
        .sort_values(
            "impact_score",
            ascending=False
        )
        .head(3)
    )

    # ----------------------------------------------------------
    # COMBINE INCIDENTS
    # ----------------------------------------------------------

    incidents = pd.concat(
        [
            high,
            medium,
            low
        ]
    )

    # Sort final cards by impact
    incidents = (
        incidents
        .sort_values(
            "impact_score",
            ascending=False
        )
        .head(10)
    )

    # ----------------------------------------------------------
    # RETURN REQUIRED COLUMNS
    # ----------------------------------------------------------

    return incidents[
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
    ]