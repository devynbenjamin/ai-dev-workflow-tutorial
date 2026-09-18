import pandas as pd
import pytest

from sales_calculations import load_data, total_sales, total_orders


def test_load_data_reads_csv_with_parsed_dates(tmp_path):
    csv_content = (
        "date,order_id,product,category,region,quantity,unit_price,total_amount\n"
        "2024-01-03,ORD-001,Widget,Electronics,North,2,10.00,20.00\n"
        "2024-01-04,ORD-002,Gadget,Accessories,South,1,15.00,15.00\n"
    )
    csv_path = tmp_path / "sales.csv"
    csv_path.write_text(csv_content)

    df = load_data(str(csv_path))

    assert len(df) == 2
    assert list(df.columns) == [
        "date", "order_id", "product", "category", "region",
        "quantity", "unit_price", "total_amount",
    ]
    assert pd.api.types.is_datetime64_any_dtype(df["date"])


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "date": pd.to_datetime(["2024-01-03", "2024-01-04", "2024-02-01", "2024-02-02"]),
        "order_id": ["ORD-001", "ORD-002", "ORD-003", "ORD-004"],
        "category": ["Electronics", "Accessories", "Electronics", "Audio"],
        "region": ["North", "South", "North", "East"],
        "total_amount": [20.00, 15.00, 30.00, 10.00],
    })


def test_total_sales_sums_all_transactions(sample_df):
    assert total_sales(sample_df) == 75.00


def test_total_orders_counts_rows(sample_df):
    assert total_orders(sample_df) == 4
