def calculate_kpis(df):

    total_sales = len(df)
    total_revenue = df["revenue"].sum()
    average_sale = df["revenue"].mean()
    total_quantity = df["quantity"].sum()
    unique_customers = df["customer_id"].nunique()

    return {
        "total_sales": total_sales,
        "total_revenue": total_revenue,
        "average_sale": average_sale,
        "total_quantity": total_quantity,
        "unique_customers": unique_customers
    }