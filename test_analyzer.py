import pytest
import pandas as pd
from analyzer import generate_data, analyse


@pytest.fixture
def df():
    return generate_data(n_rows=100)


def test_generate_data_row_count(df):
    assert len(df) == 100


def test_generate_data_columns(df):
    expected = {"order_id", "date", "product", "category", "quantity",
                "unit_price", "discount", "revenue", "region", "channel", "returned"}
    assert expected.issubset(set(df.columns))


def test_revenue_is_positive(df):
    assert (df["revenue"] > 0).all()


def test_discount_range(df):
    assert df["discount"].between(0, 0.20).all()


def test_quantity_is_positive(df):
    assert (df["quantity"] > 0).all()


def test_returned_is_boolean(df):
    assert df["returned"].dtype == bool


def test_analyse_kpis(df):
    data = analyse(df)
    kpis = data["kpis"]
    assert kpis["total_orders"] == 100
    assert kpis["total_revenue"] > 0
    assert kpis["avg_order"] > 0
    assert 0 <= kpis["return_rate"] <= 100


def test_analyse_monthly(df):
    data = analyse(df)
    assert not data["monthly"].empty


def test_analyse_top_products(df):
    data = analyse(df)
    assert len(data["top_products"]) <= 8


def test_analyse_by_category(df):
    data = analyse(df)
    assert not data["by_category"].empty


def test_analyse_by_region(df):
    data = analyse(df)
    assert not data["by_region"].empty
