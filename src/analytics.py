import pandas as pd

def calculate_category_totals(transactions_df):
    return transactions_df.groupby('category')['amount'].sum().reset_index()

def compare_budget_vs_actual(transactions_df, budget_df):
    actual = calculate_category_totals(transactions_df)
    merged = pd.merge(budget_df, actual, on='category', how='left')
    merged['amount'] = merged['amount'].fillna(0)
    merged['difference'] = merged['budget'] - merged['amount']
    return merged

def detect_overspending(budget_actual_df):
    return budget_actual_df[budget_actual_df['difference'] < 0]

def generate_suggestions(budget_actual_df):
    suggestions = []
    for _, row in budget_actual_df.iterrows():
        if row['difference'] < 0:
            suggestions.append(f"⚠️ Reduce spending in '{row['category'].title()}' by ${-row['difference']:.2f}")
        elif row['difference'] > 50:
            suggestions.append(f"💡 You could save more in '{row['category'].title()}' (${row['difference']:.2f} left)")
    return suggestions
