import pandas as pd
import pandera.pandas as pa

cleaned_weight_schema = pa.DataFrameSchema({
    "date": pa.Column(pa.DateTime),
    "weight": pa.Column(pa.Float)
})

def merge_weight_data(notion: pd.DataFrame, myfitness: pd.DataFrame) -> pd.DataFrame:
    """Merge notion and myfitnesspal weight data"""
    notion = cleaned_weight_schema.validate(notion)
    myfitness = cleaned_weight_schema.validate(myfitness)

    # Combine both datasets into one
    combined_weights = pd.concat([notion, myfitness], ignore_index=True)

    # Drop duplicates just in case
    combined_weights = combined_weights.drop_duplicates(subset='date', keep='first')

    # Sort by date
    combined_weights = combined_weights.sort_values('date').reset_index(drop=True)

    return combined_weights

    