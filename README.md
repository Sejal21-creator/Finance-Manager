# 💰 Personal Finance Advisor AI

A smart, interactive **personal finance dashboard** built using **Streamlit**, designed to help users track spending, compare budgets, detect overspending, and receive actionable financial insights.

---

## 🚀 Features

### 📊 Budget vs Actual Analysis
- Compare planned budget vs real spending
- Interactive bar charts using Plotly
- Category-wise breakdown

### 📈 Monthly Trends
- Track spending trends over time
- Category-specific analysis
- Helps identify patterns and habits

### 🚨 Overspending Alerts
- Automatically detects budget breaches
- Highlights categories where spending exceeds limits

### 💡 Smart Suggestions
- Rule-based recommendations to reduce expenses
- Category-specific financial advice

### 🎯 Goal Planning
- Set financial goals (e.g., savings target)
- Track progress with sliders and progress bars

### 🤖 AI Finance Assistant
- Simple query-based assistant
- Gives saving tips based on user input (e.g., groceries, coffee)

### 🔐 Authentication
- Basic login system using session state

---

## 🗂️ Project Structure

```text
project/
│
├── app.py                      # Main Streamlit application
├── main.py                     # CLI script to test data processing
│
├── data/
│   ├── transactions.csv        # User transaction data
│   └── budget.csv              # Budget allocation data
│
├── src/
│   ├── data_loader.py          # Load & preprocess CSV files
│   └── analytics.py            # Budget comparison & insights logic
│
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <your-repo-link>
cd project
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit app

```bash
streamlit run app.py
```

---

## 📄 Data Format

### transactions.csv

| column   | description      |
|----------|------------------|
| date     | transaction date |
| category | expense category |
| amount   | amount spent     |

### budget.csv

| column   | description               |
|----------|---------------------------|
| category | expense category          |
| budget   | allocated budget amount   |

---

## 🧠 Core Modules

### `data_loader.py`
- `load_csv(path)` → Loads CSV safely
- `preprocess_transactions(df)` → Cleans and formats transaction data
- `preprocess_budget(df)` → Cleans budget data

### `analytics.py`
- `compare_budget_vs_actual()` → Merges & compares data
- `detect_overspending()` → Finds budget violations
- `generate_suggestions()` → Provides insights

---

## 🖥️ CLI Testing (Optional)

You can test preprocessing without UI:

```bash
python main.py
```

This will:
- Load CSV files
- Process them
- Print sample output

---

## ⚠️ Limitations

- Authentication is basic (hardcoded users)
- AI assistant is rule-based (not ML-powered yet)
- No database integration (uses CSV only)

---

## 🔮 Future Improvements

- Add real authentication (JWT / OAuth)
- Integrate database (PostgreSQL / MongoDB)
- Use ML for predictive spending insights
- Deploy on cloud (AWS / GCP)
- Add real chatbot using LLM APIs

---

## 💡 Tech Stack

- Python
- Streamlit
- Pandas
- Plotly

---

## 🎯 Use Case

This project helps individuals:
- Track expenses
- Stay within budget
- Improve financial discipline
- Plan future savings effectively

---

## 👨‍💻 Author

Built as a **Personal Finance AI Project** to demonstrate:
- Data analysis skills
- Dashboard development
- Real-world problem solving

