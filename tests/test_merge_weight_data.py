import pytest 
import pandas as pd
import pandera.errors as perrors 
from src.merge_weight_data import merge_weight_data, cleaned_weight_schema

class Test_merge_weight_data():

    valid_notion = pd.DataFrame({
        "date": ["2025-01-01", "2025-01-02"],
        "weight": [70.0, 71.0]
    })
    valid_notion["date"] = pd.to_datetime(valid_notion["date"])
    valid_myfitness = pd.DataFrame({
        "date": ["2025-01-01", "2025-01-02"],
        "weight": [70.0, 71.0]
    })
    valid_myfitness["date"] = pd.to_datetime(valid_myfitness["date"])

    def test_schema_validation(self):
        notion = self.valid_notion
        myfitness = self.valid_myfitness
        notion = cleaned_weight_schema.validate(notion)
        myfitness = cleaned_weight_schema.validate(myfitness)

        combined_weights = merge_weight_data(notion, myfitness)
        # breakpoint()
        assert combined_weights.shape == (2, 2)
        assert list(combined_weights.columns) == ["date", "weight"]
        assert pd.api.types.is_datetime64_any_dtype(combined_weights["date"])
        assert pd.api.types.is_float_dtype(combined_weights["weight"])
