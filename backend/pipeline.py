import pandas as pd

def clean_data(df):

    df = df.drop_duplicates()

    df.columns = [c.strip().lower() for c in df.columns]

    for col in df.select_dtypes(include="number"):
        df[col] = df[col].fillna(df[col].mean())

    for col in df.select_dtypes(include="object"):
        df[col] = df[col].fillna("Unknown")

    return df
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
