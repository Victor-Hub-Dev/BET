import streamlit as st
import pandas as pd
from datetime import datetime

# Simulate a database with a dictionary
data = {
    'users': [],
    'expenses': [],
    'budgets': []
}

def register_user(username, password):
    data['users'].append({'username': username, 'password': password})

def add_expense(username, amount, category, date):
    data['expenses'].append({'username': username, 'amount': amount, 'category': category, 'date': date})

def add_budget(username, category, budget_amount):
    data['budgets'].append({'username': username, 'category': category, 'budget_amount': budget_amount})

def get_expenses(username):
    return [expense for expense in data['expenses'] if expense['username'] == username]

def get_budgets(username):
    return [budget for budget in data['budgets'] if budget['username'] == username]

# Streamlit UI
st.title("Budgeting and Expense Tracking App")

# User Registration
st.sidebar.header("User Registration")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")
if st.sidebar.button("Register"):
    register_user(username, password)
    st.sidebar.success("User registered!")

# User Login
st.sidebar.header("User Login")
login_username = st.sidebar.text_input("Login Username")
login_password = st.sidebar.text_input("Login Password", type="password")
login_user = next((user for user in data['users'] if user['username'] == login_username and user['password'] == login_password), None)
if st.sidebar.button("Login"):
    if login_user:
        st.sidebar.success("Logged in as {}".format(login_username))
    else:
        st.sidebar.error("Invalid credentials")

if login_user:
    st.header("Welcome, {}".format(login_username))

    # Add Expense
    st.subheader("Add Expense")
    expense_amount = st.number_input("Amount", min_value=0.0)
    expense_category = st.selectbox("Category", ["Food", "Transport", "Entertainment", "Utilities", "Others"])
    expense_date = st.date_input("Date", datetime.now())
    if st.button("Add Expense"):
        add_expense(login_username, expense_amount, expense_category, expense_date)
        st.success("Expense added!")

    # Add Budget
    st.subheader("Set Budget")
    budget_category = st.selectbox("Budget Category", ["Food", "Transport", "Entertainment", "Utilities", "Others"])
    budget_amount = st.number_input("Budget Amount", min_value=0.0, key="budget_amount")
    if st.button("Set Budget"):
        add_budget(login_username, budget_category, budget_amount)
        st.success("Budget set!")

    # View Expenses
    st.subheader("View Expenses")
    expenses = get_expenses(login_username)
    expenses_df = pd.DataFrame(expenses)
    if not expenses_df.empty:
        st.table(expenses_df)

    # View Budgets
    st.subheader("View Budgets")
    budgets = get_budgets(login_username)
    budgets_df = pd.DataFrame(budgets)
    if not budgets_df.empty:
        st.table(budgets_df)

    # Analytics
    st.subheader("Expense Analytics")
    if not expenses_df.empty:
        expenses_summary = expenses_df.groupby("category")["amount"].sum().reset_index()
        st.bar_chart(expenses_summary.set_index("category"))

