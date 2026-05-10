
import pandas as pd
import os

def load_csv(filepath):
    """Load a CSV file into a pandas DataFrame."""
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return None
    try:
        df = pd.read_csv(filepath)
        print(f"✅ Loaded: {filepath}")
        return df
    except Exception as e:
        print(f"❌ Error loading {filepath}: {e}")
        return None

def preprocess_transactions(df):
    """Clean and prepare the transactions data."""
    df.columns = df.columns.str.strip().str.lower()

    # Convert and clean columns
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')

    for col in ['description', 'type', 'category', 'account']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.lower().fillna("unknown")

    # Drop rows with missing essential data
    df = df.dropna(subset=['date', 'amount', 'category'])

    return df

def preprocess_budget(df):
    """Clean and prepare the budget data."""
    df.columns = df.columns.str.strip().str.lower()

    df['category'] = df['category'].astype(str).str.strip().str.lower().fillna("unknown")
    df['budget'] = pd.to_numeric(df['budget'], errors='coerce')

    df = df.dropna(subset=['category', 'budget'])

    return df
