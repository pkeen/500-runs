import pandas as pd
import pandera.pandas as pa

notion_data_schema = pa.DataFrameSchema({
    "Date": pa.Column(pa.String, nullable=True),         # ← allow null
    "Weight KG": pa.Column(pa.Float, nullable=True, coerce=True)
})

def clean_notion_weight_data(df: pd.DataFrame):
    """Pipeline for cleaning notion weight data"""

    # validate key columns
    df = notion_data_schema.validate(df)

    # Step 1: Extract just the date and weight columns
    notion_weight_df = df[['Date', 'Weight KG']].copy()

    # Step 2: Convert 'Date' to datetime format
    notion_weight_df['Date'] = pd.to_datetime(notion_weight_df['Date'], errors='coerce')

    # Step 3: Drop any rows where date or weight is missing
    notion_weight_df = notion_weight_df.dropna(subset=['Date', 'Weight KG'])

    # Step 4: Sort by date (optional but useful for visualizations later)
    notion_weight_df = notion_weight_df.sort_values(by='Date').reset_index(drop=True)

    # Optional: Rename columns to standardize for merging later
    notion_weight_df.rename(columns={'Date': 'date', 'Weight KG': 'weight'}, inplace=True)

    return notion_weight_df
