import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import time

# ----------------------------------------
# Authentication (Disabled for Demo Use)
# ----------------------------------------

# import streamlit_authenticator as stauth

# credentials = {
#     "usernames": {
#         "admin": {
#             "name": "HR Admin",
#             "password": "admin123"
#         }
#     }
# }

# authenticator = stauth.Authenticate(
#     credentials,
#     "hr_dashboard_cookie",
#     "random_signature_key",
#     cookie_expiry_days=1
# )

# def authenticate_user():
#     login_result = authenticator.login(location="main", key="auth")
#     if login_result:
#         name, authentication_status, username = login_result
#         if authentication_status:
#             authenticator.logout("Logout", "sidebar")
#             st.sidebar.success(f"Welcome {name} 👋")
#             return True
#         elif authentication_status is False:
#             st.error("Username/password is incorrect")
#         elif authentication_status is None:
#             st.warning("Please enter your username and password")
#     else:
#         st.warning("Login form not rendered correctly.")
#     return False

# ----------------------------------------
# Configuration
# ----------------------------------------

# Backend API base URL
API_BASE = "https://hr-analytics-dashboard.onrender.com"

# ----------------------------------------
# Helper Function: Retry API requests
# ----------------------------------------


def fetch_with_retry(endpoint, retries=3, delay=1):
    """
    Tries to fetch data from the API with retries on failure.
    """
    url = f"{API_BASE}{endpoint}"
    for attempt in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                st.error(f"Error fetching data from {endpoint}: {e}")
                st.stop()

# ----------------------------------------
# Component: KPI Metrics
# ----------------------------------------


def render_kpi_summary():
    """
    Displays high-level KPIs like headcount, average age, and tenure.
    """
    with st.spinner("Loading KPI summary..."):
        data = fetch_with_retry("/kpi-summary")
        col1, col2, col3 = st.columns(3)
        col1.metric("Headcount", data['headcount'])
        col2.metric("Avg Tenure", data['avg_tenure'])
        col3.metric("Avg Age", data['avg_age'])

# ----------------------------------------
# Component: Department Summary Chart
# ----------------------------------------


def render_department_chart():
    """
    Displays a combo bar + line chart showing headcount vs. avg income per department.
    """
    dept_data = pd.DataFrame(fetch_with_retry("/departments"))
    fig = px.bar(dept_data, x="department", y="headcount",
                 title="Headcount and Avg Income by Department")
    fig.add_scatter(x=dept_data['department'], y=dept_data['avg_income'],
                    name="Avg Income", yaxis="y2")
    fig.update_layout(yaxis2=dict(overlaying='y', side='right'))
    st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------
# Component: Attrition Rate KPIs
# ----------------------------------------


def render_attrition_metrics():
    """
    Shows attrition rates segmented by filters like gender and department.
    """
    st.subheader("Attrition Rates")
    total = fetch_with_retry("/attrition-rate")['attrition_rate']
    female = fetch_with_retry("/attrition-rate?gender=Female")['attrition_rate']
    sales = fetch_with_retry("/attrition-rate?department=Sales")['attrition_rate']
    male_rnd = fetch_with_retry("/attrition-rate?gender=Male&department=Research%20%26%20Development")['attrition_rate']

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total", f"{total}%")
    col2.metric("Female", f"{female}%")
    col3.metric("Sales", f"{sales}%")
    col4.metric("Male in R&D", f"{male_rnd}%")

# ----------------------------------------
# Component: Employee Table & Charts
# ----------------------------------------


def render_employee_data():
    """
    Loads and visualizes the entire employee dataset,
    including raw table and charts by department/gender/attrition.
    """
    st.subheader("Employee Data")
    raw = fetch_with_retry("/employees")

    if isinstance(raw, list) and all(isinstance(row, dict) for row in raw):
        df = pd.DataFrame(raw)
        st.dataframe(df, use_container_width=True)

        st.subheader("Distributions")
        col1, col2 = st.columns(2)

        fig1 = px.histogram(df, x="department", color="attrition",
                            barmode="group", title="Attrition by Department")
        col1.plotly_chart(fig1, use_container_width=True)

        fig2 = px.histogram(df, x="department", color="gender",
                            barmode="group", title="Gender by Department")
        col2.plotly_chart(fig2, use_container_width=True)
    else:
        st.error("⚠️ Could not fetch employee data.")
        st.write("Raw response:", raw)

# ----------------------------------------
# App Entry Point
# ----------------------------------------

# Replace this with authentication check in production
# if authenticate_user():


with st.spinner("Loading dashboard..."):
    st.title("HR Dashboard")
    render_kpi_summary()
    render_department_chart()
    render_attrition_metrics()
    render_employee_data()