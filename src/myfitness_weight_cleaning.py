import pandas as pd
import pandera.pandas as pa

myfitness_data_schema = pa.DataFrameSchema({
    "Date": pa.Column(pa.String, nullable=True),         # ← allow null
    "Weight": pa.Column(pa.Float, nullable=True, coerce=True)
})


def clean_myfitness_weight_data(df: pd.DataFrame):
    """Pipeline for cleaning myfitnesspal weight data"""

    # validate key columns
    df = myfitness_data_schema.validate(df)

    # Step 1: Extract just the date and weight columns
    myfitness_weight_df = df[['Date', 'Weight']].copy()

    # Step 2: Convert 'Date' to datetime format
    myfitness_weight_df['Date'] = pd.to_datetime(myfitness_weight_df['Date'], errors='coerce')

    # Step 3: Drop any rows where date or weight is missing
    myfitness_weight_df = myfitness_weight_df.dropna(subset=['Date', 'Weight'])

    # Step 4: Sort by date (optional but useful for visualizations later)
    myfitness_weight_df = myfitness_weight_df.sort_values(by='Date').reset_index(drop=True)

    # Optional: Rename columns to standardize for merging later
    myfitness_weight_df.rename(columns={'Date': 'date', 'Weight': 'weight'}, inplace=True)

    return myfitness_weight_df

