from src.data_loader import load_csv, preprocess_transactions, preprocess_budget

def main():
    # Paths to your data files
    transactions_path = "data/transactions.csv"
    budget_path = "data/budget.csv"

    # Load CSV files
    transactions_df = load_csv(transactions_path)
    budget_df = load_csv(budget_path)

    # Preprocess CSV files
    if transactions_df is not None:
        transactions_df = preprocess_transactions(transactions_df)
        print("\n📄 Processed Transactions Data:")
        print(transactions_df.head())

    if budget_df is not None:
        budget_df = preprocess_budget(budget_df)
        print("\n📊 Processed Budget Data:")
        print(budget_df.head())

if __name__ == "__main__":
    main()
