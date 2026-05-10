## app.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from streamlit.components.v1 import html
from src.data_loader import load_csv, preprocess_transactions, preprocess_budget
from src.analytics import compare_budget_vs_actual, detect_overspending, generate_suggestions

# User authentication
users = {"admin": "1234", "user": "pass"}
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if not st.session_state.authenticated:
    st.title("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in users and users[username] == password:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Invalid username or password")
    st.stop()

# Set page config
st.set_page_config(
    page_title="💰 Personal Finance Advisor AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom minimal UI
st.markdown("""
<style>
    body { background-color: #ffffff; color: #222222; font-family: 'Segoe UI', sans-serif; }
    .block-container { padding: 2rem; }
    .stTabs [data-baseweb="tab"] {
        background-color: #e4f0ff;
        border-radius: 10px 10px 0 0;
        margin-right: 8px;
        padding: 12px 30px;
        font-weight: 700;
        font-size: 1.1rem;
        color: #1a73e8;
        cursor: pointer;
        transition: all 0.35s ease;
        box-shadow: 0 2px 5px rgba(26, 115, 232, 0.15);
        user-select: none;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #bbd7ff;
        transform: scale(1.1);
        box-shadow: 0 4px 15px rgba(26, 115, 232, 0.35);
    }
    .stTabs [aria-selected="true"] {
        background-color: #ffffff;
        border-bottom: 4px solid #1a73e8;
        color: #0c47b7;
        box-shadow: 0 6px 20px rgba(26, 115, 232, 0.5);
        transform: scale(1.15);
        font-weight: 800;
    }
</style>
""", unsafe_allow_html=True)

# Tabs
main_tabs = st.tabs(["🏠 Home", "📊 Budget vs Actual", "📈 Monthly Trends", "🚨 Alerts & Suggestions", "🎯 Goal Planning", "🤖 AI Assistant"])

# Load Data
transactions = preprocess_transactions(load_csv("data/transactions.csv"))
budget = preprocess_budget(load_csv("data/budget.csv"))

# Filters
st.sidebar.header("📅 Filter Options")
date_range = st.sidebar.date_input("Select Date Range", [transactions['date'].min(), transactions['date'].max()])

if len(date_range) == 2:
    start_date, end_date = date_range
    transactions = transactions[(transactions['date'] >= pd.Timestamp(start_date)) & (transactions['date'] <= pd.Timestamp(end_date))]

categories = sorted(transactions['category'].unique())
selected_categories = st.sidebar.multiselect("Select Categories", categories, default=categories)
transactions = transactions[transactions['category'].isin(selected_categories)]
budget = budget[budget['category'].isin(selected_categories)]

# Analytics
comparison_df = compare_budget_vs_actual(transactions, budget)
overspending = detect_overspending(comparison_df)
suggestions = generate_suggestions(comparison_df)

# 🏠 Home
with main_tabs[0]:
    st.title("🏠 Welcome to Your Finance Dashboard")
    st.markdown("""
        Manage your personal finances using interactive analytics:
        - 📊 Compare **budget vs. actual** spending
        - 🔮 Forecast **category trends** over time
        - 🚨 Get **overspending alerts** and suggestions
        - 🎯 Plan and track **financial goals**
        - 🤖 Chat with your AI finance assistant
    """)

# 📊 Budget vs Actual
with main_tabs[1]:
    st.subheader("📊 Budget vs Actual Spending")
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=comparison_df['category'],
        y=comparison_df['budget'],
        name='Budget',
        marker_color='lightblue',
        text=comparison_df['budget'],
        textposition='auto',
        hovertemplate='Budget: $%{y:.2f}'
    ))
    fig.add_trace(go.Bar(
        x=comparison_df['category'],
        y=comparison_df['amount'],
        name='Actual',
        marker_color='salmon',
        text=comparison_df['amount'],
        textposition='auto',
        hovertemplate='Actual: $%{y:.2f}'
    ))
    fig.update_layout(
        barmode='group',
        xaxis_tickangle=-30,
        yaxis_title='Amount ($)',
        transition_duration=500,
        height=500,
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    st.plotly_chart(fig, use_container_width=True)

# 📈 Monthly Trends
with main_tabs[2]:
    st.subheader("📈 Monthly Category Trends")
    transactions['month'] = transactions['date'].dt.to_period('M').astype(str)
    monthly = transactions.groupby(['month', 'category'])['amount'].sum().reset_index()
    selected = st.selectbox("Select a category", selected_categories)
    trend = monthly[monthly['category'] == selected]
    fig2 = go.Figure(go.Scatter(
        x=trend['month'],
        y=trend['amount'],
        mode='lines+markers',
        line=dict(color='mediumblue'),
        fill='tozeroy',
        hovertemplate='%{x}: $%{y:.2f}'
    ))
    fig2.update_layout(yaxis_title='Amount ($)', transition_duration=500)
    st.plotly_chart(fig2, use_container_width=True)

# 🚨 Alerts & Suggestions
with main_tabs[3]:
    st.subheader("🚨 Overspending Alerts & Suggestions")
    if overspending.empty:
        st.success("✅ All categories are within budget!")
    else:
        for _, row in overspending.iterrows():
            st.error(f"Over in {row['category']}: Spent ${row['amount']} vs Budget ${row['budget']}")
    st.markdown("---")
    st.subheader("💡 Suggestions")
    if suggestions:
        for tip in suggestions:
            st.info(tip)
    else:
        st.info("You're doing great! No suggestions needed.")

# 🎯 Goal Planning
with main_tabs[4]:
    st.subheader("🎯 Financial Goal Planning")
    if "goals" not in st.session_state:
        st.session_state.goals = []
    with st.form("goal_form"):
        name = st.text_input("Goal Name")
        amount = st.number_input("Target Amount ($)", min_value=1.0)
        deadline = st.date_input("Deadline")
        submitted = st.form_submit_button("Add Goal")
        if submitted and name:
            st.session_state.goals.append({"name": name, "amount": amount, "deadline": deadline, "progress": 0})
            st.success("Goal added successfully!")

    for idx, goal in enumerate(st.session_state.goals):
        st.write(f"**{goal['name']}** | Target: ${goal['amount']} | Deadline: {goal['deadline']}")
        progress = st.slider(f"Progress toward {goal['name']}", 0, int(goal['amount']), int(goal['progress']), key=f"progress_{idx}")
        goal['progress'] = progress
        st.progress(progress / goal['amount'])

# 🤖 AI Assistant
with main_tabs[5]:
    st.subheader("🤖 AI Finance Assistant")
    query = st.text_input("Ask about saving tips or spending advice by category")
    tips = {
        "restaurants": "🍽️ Try home-cooked meals and reduce eating out.",
        
        "groceries": "🛒 Plan your meals and shop with a list to avoid impulse buys.",
        "utilities": "💡 Unplug unused devices and switch to energy-efficient appliances.",
        "gas": "⛽ Use apps to find the cheapest fuel and carpool if possible.",
        "entertainment": "🎬 Use free or low-cost events like parks and online content.",
        "coffee": "☕ Brew your own coffee instead of visiting shops daily.",
        "subscriptions": "📦 Review monthly charges and cancel unused subscriptions.",
        "alcohol": "🍷 Buy alcohol from stores instead of bars or restaurants.",
        "fast food": "🍔 Limit fast food to once a week and opt for healthy snacks.",
        "travel": "✈️ Plan in advance, use comparison tools, and look for travel deals.",
        "shopping": "🛍️ Make a list and avoid impulse buying, use coupons or sales.",
        "health": "💊 Use preventive care, compare medicine prices online.",
        "education": "🎓 Explore scholarships, open courses, and student discounts.",
        "misc": "💼 Track miscellaneous expenses monthly and categorize where possible."
    }
    if query:
        matched = False
        for cat in tips:
            if cat in query.lower():
                st.success(tips[cat])
                matched = True
                break
        if not matched:
            st.warning("No specific tip found. Try asking about groceries, gas, or entertainment.")
    st.markdown("---")
    st.caption("This assistant can give tailored tips per category. Try: 'How to save on coffee?' or 'Advice for grocery spending'")










