def generate_recommendation(df):

    anomalies = df[df["is_anomaly"] == 1]

    if anomalies.empty:
        return "No action is required because no significant anomalies were detected."

    top_anomaly = anomalies.sort_values(
        "impact_score",
        ascending=False
    ).iloc[0]

    region = top_anomaly["region"]
    category = top_anomaly["category"]
    product = top_anomaly["product"]
    quantity = top_anomaly["quantity"]
    unit_price = top_anomaly["unit_price"]
    revenue = top_anomaly["revenue"]
    impact = top_anomaly["impact_score"]

    # Check whether the same business combination appears repeatedly
    driver_count = len(
        anomalies[
            (anomalies["region"] == region) &
            (anomalies["category"] == category) &
            (anomalies["product"] == product)
        ]
    )

    if quantity >= 15:
        recommendation = (
            f"Investigate unusually high quantity for {product} "
            f"in the {region} region. Review whether this represents "
            f"a bulk order, unusual demand, or a data-entry issue."
        )

    elif unit_price >= 40000:
        recommendation = (
            f"Review the pricing of {product} in the {region} region. "
            f"The high unit price contributed significantly to the "
            f"unusual revenue value. Check pricing rules, discounts, "
            f"and transaction records."
        )

    elif driver_count >= 3:
        recommendation = (
            f"Investigate the repeated {product} anomaly pattern in "
            f"the {region} region. {driver_count} similar anomalies "
            f"were detected, suggesting this may be a recurring "
            f"business pattern rather than an isolated transaction."
        )

    elif revenue >= 450000:
        recommendation = (
            f"Review the high-value {product} transaction in the "
            f"{region} region. Check customer activity, pricing, "
            f"quantity, and transaction records for the source of "
            f"the unusual revenue."
        )

    elif impact >= 70:
        recommendation = (
            f"Prioritize investigation of {product} in the {region} "
            f"region and review the related {category} transactions "
            f"for unusual business activity."
        )

    else:
        recommendation = (
            f"Continue monitoring {product} sales in the {region} "
            f"region for additional unusual activity."
        )

    return recommendation