import pandas as pd


def load_data(path):
    return pd.read_csv(path, parse_dates=["date"])


def total_sales(df):
    return df["total_amount"].sum()


def total_orders(df):
    return len(df)


def monthly_trend(df):
    return (
        df.assign(month=df["date"].dt.to_period("M").astype(str))
        .groupby("month", as_index=False)["total_amount"]
        .sum()
        .sort_values("month")
        .reset_index(drop=True)
    )
