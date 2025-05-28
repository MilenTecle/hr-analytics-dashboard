import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# --- TEMPORARILY DISABLED AUTHENTICATION ---
# import streamlit_authenticator as stauth

# ------------------------
# Authentication Setup
# ------------------------
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
#             st.sidebar.success(f"Welcome {name} \U0001F44B")
#             return True
#         elif authentication_status is False:
#             st.error("Username/password is incorrect")
#         elif authentication_status is None:
#             st.warning("Please enter your username and password")
#     else:
#         st.warning("Login form not rendered correctly.")
#     return False

# ------------------------
# API Utilities
# ------------------------


API_BASE = "https://hr-analytics-dashboard.onrender.com"


def fetch_api_data(endpoint):
    try:
        response = requests.get(f"{API_BASE}{endpoint}", timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error fetching data from {endpoint}: {e}")
        return None

# ------------------------
# Dashboard Components
# ------------------------


def render_kpi_summary():
    data = fetch_api_data("/kpi-summary")
    if not data:
        return

    col1, col2, col3 = st.columns(3)
    col1.metric("Headcount", data['headcount'])
    col2.metric("Avg Tenure", data['avg_tenure'])
    col3.metric("Avg Age", data['avg_age'])

def render_department_chart():
    data = fetch_api_data("/departments")
    if not data:
        return

    df = pd.DataFrame(data)
    fig = px.bar(df, x="department", y="headcount", title="Headcount and Avg Income by Department")
    fig.add_scatter(x=df['department'], y=df['avg_income'], name="Avg Income", yaxis="y2")
    fig.update_layout(yaxis2=dict(overlaying='y', side='right'))
    st.plotly_chart(fig, use_container_width=True)

def render_attrition_metrics():
    st.subheader("Attrition Rates")

    total = fetch_api_data("/attrition-rate")
    female = fetch_api_data("/attrition-rate?gender=Female")
    sales = fetch_api_data("/attrition-rate?department=Sales")
    male_rnd = fetch_api_data("/attrition-rate?gender=Male&department=Research%20%26%20Development")

    if not all([total, female, sales, male_rnd]):
        return

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total", f"{total['attrition_rate']}%")
    col2.metric("Female", f"{female['attrition_rate']}%")
    col3.metric("Sales", f"{sales['attrition_rate']}%")
    col4.metric("Male in R&D", f"{male_rnd['attrition_rate']}%")

def render_employee_data():
    st.subheader("Employee Data")
    raw = fetch_api_data("/employees")

    if not raw or not isinstance(raw, list):
        st.warning("No valid employee data returned.")
        return

    df = pd.DataFrame(raw)
    st.dataframe(df, use_container_width=True)

    st.subheader("Distributions")
    col1, col2 = st.columns(2)

    fig1 = px.histogram(df, x="department", color="attrition", barmode="group", title="Attrition by Department")
    col1.plotly_chart(fig1, use_container_width=True)

    fig2 = px.histogram(df, x="department", color="gender", barmode="group", title="Gender by Department")
    col2.plotly_chart(fig2, use_container_width=True)

# ------------------------
# Run App
# ------------------------


st.title("HR Dashboard")

# if authenticate_user():
with st.spinner("Loading KPI Summary..."):
    render_kpi_summary()

with st.spinner("Loading Department Chart..."):
    render_department_chart()

with st.spinner("Loading Attrition Rates..."):
    render_attrition_metrics()

with st.spinner("Loading Employee Data..."):
    render_employee_data()
