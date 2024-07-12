import streamlit as st
import pandas as pd
from datetime import datetime

# Simulate a database with a dictionary
data = {
    'users': [],
    'expenses': [],
    'budgets': []
}

# User registration function
def register_user(username, password):
    if any(user['username'] == username for user in data['users']):
        st.error(f"User '{username}' already exists.")
    else:
        data['users'].append({'username': username, 'password': password})
        st.success(f"User '{username}' registered successfully")
    st.write("Current Users:", data['users'])

# User authentication function
def authenticate_user(username, password):
    user = next((user for user in data['users'] if user['username'] == username and user['password'] == password), None)
    return user

# Function to add expense
def add_expense(username, amount, category, date):
    data['expenses'].append({'username': username, 'amount': amount, 'category': category, 'date': date})

# Function to add budget
def add_budget(username, category, budget_amount):
    data['budgets'].append({'username': username, 'category': category, 'budget_amount': budget_amount})

# Function to get expenses
def get_expenses(username):
    return [expense for expense in data['expenses'] if expense['username'] == username]

# Function to get budgets
def get_budgets(username):
    return [budget for budget in data['budgets'] if budget['username'] == username]

# Streamlit UI
st.title("Budgeting and Expense Tracking App")

# User Registration
st.sidebar.header("User Registration")
reg_username = st.sidebar.text_input("Register Username", key="reg_username")
reg_password = st.sidebar.text_input("Register Password", type="password", key="reg_password")
if st.sidebar.button("Register"):
    register_user(reg_username, reg_password)

# User Login
st.sidebar.header("User Login")
login_username = st.sidebar.text_input("Login Username", key="login_username")
login_password = st.sidebar.text_input("Login Password", type="password", key="login_password")
if st.sidebar.button("Login"):
    login_user = authenticate_user(login_username, login_password)
    st.write(f"Attempting to log in with username: {login_username} and password: {login_password}")
    st.write(f"Users in data: {data['users']}")
    st.write(f"Login user found: {login_user}")
    if login_user:
        st.session_state.username = login_username
        st.sidebar.success(f"Logged in as {login_username}")
    else:
        st.sidebar.error("Invalid credentials")

# Debug: Print users data
st.sidebar.write("Registered Users:", data['users'])

# Check if user is logged in
if 'username' in st.session_state:
    st.header(f"Welcome, {st.session_state.username}")

    # Add Expense
    st.subheader("Add Expense")
    expense_amount = st.number_input("Amount", min_value=0.0)
    expense_category = st.selectbox("Category", ["Food", "Transport", "Entertainment", "Utilities", "Others"])
    expense_date = st.date_input("Date", datetime.now())
    if st.button("Add Expense"):
        add_expense(st.session_state.username, expense_amount, expense_category, expense_date)
        st.success("Expense added!")

    # Add Budget
    st.subheader("Set Budget")
    budget_category = st.selectbox("Budget Category", ["Food", "Transport", "Entertainment", "Utilities", "Others"])
    budget_amount = st.number_input("Budget Amount", min_value=0.0, key="budget_amount")
    if st.button("Set Budget"):
        add_budget(st.session_state.username, budget_category, budget_amount)
        st.success("Budget set!")

    # View Expenses
    st.subheader("View Expenses")
    expenses = get_expenses(st.session_state.username)
    expenses_df = pd.DataFrame(expenses)
    if not expenses_df.empty:
        st.table(expenses_df)

    # View Budgets
    st.subheader("View Budgets")
    budgets = get_budgets(st.session_state.username)
    budgets_df = pd.DataFrame(budgets)
    if not budgets_df.empty:
        st.table(budgets_df)

    # Analytics
    st.subheader("Expense Analytics")
    if not expenses_df.empty:
        expenses_summary = expenses_df.groupby("category")["amount"].sum().reset_index()
        st.bar_chart(expenses_summary.set_index("category"))
else:
    st.header("Please log in to use the app")
