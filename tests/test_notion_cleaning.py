import pytest 
import pandera.errors as perrors 
from src.notion_data_cleaning import clean_notion_weight_data, notion_data_schema
import pandas as pd


class Test_clean_notion_weight_data: 
    def test_notion_validation(self):
        """does this print out?"""
        df = pd.DataFrame({
            "Date": ["2025-01-01", "2025-01-02", "2025-01-03"],
            "Weight KG": [90, 91, 92]
        })
        df = clean_notion_weight_data(df)
        
    def test_invalid_column_raises(self):
        """does this print out?"""
        df = pd.DataFrame({
            "Date": ["2025-01-01", "2025-01-02", "2025-01-03"],
            "Weight LBS": [90, 91, 92]
        })
        with pytest.raises(perrors.SchemaError):
            df = clean_notion_weight_data(df)

    def test_invalid_dtype_raises(self):
        df = pd.DataFrame({
            "Date": ["2025-01-01", "2025-01-02"],
            "Weight KG": ["seventy", "eighty"]
        })

        with pytest.raises(perrors.SchemaError):
            clean_notion_weight_data(df)

    def test_clean_valid_data(self):
        df = pd.DataFrame({
            "Date": ["2025-01-01", "2025-01-02"],
            "Weight KG": [70.5, 71.0]
        })
        cleaned = clean_notion_weight_data(df)

        assert cleaned.shape == (2, 2)
        assert list(cleaned.columns) == ["date", "weight"]
        assert pd.api.types.is_datetime64_any_dtype(cleaned["date"])
        assert pd.api.types.is_float_dtype(cleaned["weight"])

    def test_rows_with_nans_are_dropped(self):
        df = pd.DataFrame({
            "Date": ["2025-01-01", None, "2025-01-03"],
            "Weight KG": [70.0, 71.0, None]
        })
        cleaned = clean_notion_weight_data(df)

        # Only first row is valid
        assert cleaned.shape[0] == 1
        assert cleaned.iloc[0]["weight"] == 70.0

    def test_missing_columns(self):
        df = pd.DataFrame({
            "Date": ["2025-01-01"],
            # "Weight KG" column is missing
        })

        with pytest.raises(perrors.SchemaError):
            clean_notion_weight_data(df)

    def test_column_renaming(self):
        df = pd.DataFrame({
            "Date": ["2025-01-01"],
            "Weight KG": [70.0]
        })
        cleaned = clean_notion_weight_data(df)
        assert "date" in cleaned.columns
        assert "weight" in cleaned.columns
        assert "Date" not in cleaned.columns
        assert "Weight KG" not in cleaned.columns
