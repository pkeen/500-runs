import pytest 
import pandas as pd
import pandera.errors as perrors 
from src.myfitness_weight_cleaning import myfitness_data_schema, clean_myfitness_weight_data
import pdb  

class Test_clean_myfitness_weight_data:
    def test_myfitness_validation(self):
        df = pd.DataFrame({
            "Date": ["2025-01-01", "2025-01-02", "2025-01-03"],
            "Weight": [90, 91, 92]
        })
        df = clean_myfitness_weight_data(df)
        assert df.shape == (3, 2)
        assert list(df.columns) == ["date", "weight"]
        assert pd.api.types.is_datetime64_any_dtype(df["date"])
        # breakpoint()
        assert pd.api.types.is_float_dtype(df["weight"])
    
    def test_invalid_column_raises(self):
        df = pd.DataFrame({
            "Date": ["2025-01-01", "2025-01-02", "2025-01-03"],
            "Weight LBS": [90, 91, 92]
        })
        with pytest.raises(perrors.SchemaError):
            df = clean_myfitness_weight_data(df)

    def test_invalid_dtype_raises(self):    
        df = pd.DataFrame({
            "Date": ["2025-01-01", "2025-01-02"],
            "Weight": ["seventy", "eighty"]
        })

        with pytest.raises(perrors.SchemaError):
            clean_myfitness_weight_data(df)