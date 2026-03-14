import pandas as pd

def clean_data(df, config):

    if config.get("remove_duplicates"):
        df = df.drop_duplicates()

    strategy = config.get("missing_strategy")

    if strategy == "mean":
        for col in df.select_dtypes(include="number"):
            df[col] = df[col].fillna(df[col].mean())

    elif strategy == "median":
        for col in df.select_dtypes(include="number"):
            df[col] = df[col].fillna(df[col].median())

    if config.get("normalize_text"):
        for col in df.select_dtypes(include="object"):
            df[col] = df[col].str.lower()

    df.columns = [c.strip().lower() for c in df.columns]

    return df
def profile_data(df):

    profile = {}

    profile["rows"] = len(df)
    profile["columns"] = len(df.columns)
    profile["missing_values"] = int(df.isnull().sum().sum())
    profile["duplicate_rows"] = int(df.duplicated().sum())

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    categorical_cols = df.select_dtypes(include="object").columns.tolist()

    profile["numeric_columns"] = numeric_cols
    profile["categorical_columns"] = categorical_cols

    return profile
def generate_insights(df):

    insights = {}

    insights["rows"] = len(df)
    insights["columns"] = len(df.columns)
    insights["missing_values"] = int(df.isnull().sum().sum())

    numeric = df.select_dtypes(include="number")

    if not numeric.empty:
        insights["summary"] = numeric.describe().to_dict()

        insights["correlation"] = numeric.corr().to_dict()

    categorical = df.select_dtypes(include="object")

    top_categories = {}

    for col in categorical.columns:
        top_categories[col] = df[col].value_counts().head(5).to_dict()

    insights["top_categories"] = top_categories

    return insights
