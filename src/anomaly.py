from sklearn.ensemble import IsolationForest


def detect_anomalies(df):

    features = df[["quantity", "unit_price", "revenue"]]

    model = IsolationForest(
        contamination=0.02,
        random_state=42
    )

    # Detect normal/anomalous transactions
    predictions = model.fit_predict(features)

    df["is_anomaly"] = (predictions == -1).astype(int)

    # Continuous anomaly score
    df["anomaly_score"] = model.decision_function(features)

    # Convert to anomaly strength
    df["anomaly_strength"] = (
        -df["anomaly_score"]
    ).clip(lower=0)

    return df