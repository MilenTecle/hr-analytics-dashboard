import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import streamlit_authenticator as stauth


# Credentials
credentials = {
    "usernames": {
        "admin": {
            "name": "HR Admin",
            "password": "admin123"
        }
    }
}

# Setup
authenticator = stauth.Authenticate(
    credentials,
    "hr_dashboard_cookie",
    "random_signature_key",
    cookie_expiry_days=1
)

# This now works with the GitHub version
name, authentication_status, username = authenticator.login(
    form_name="Login", location="main"
)

if authentication_status is False:
    st.error("Username/password is incorrect")
elif authentication_status is None:
    st.warning("Please enter your username and password")
elif authentication_status:
    authenticator.logout("Logout", "sidebar")
    st.sidebar.success(f"Welcome {name} 👋")
    st.write("Dashboard content goes here.")

    # Main HR Dashboard App
    # -----------------------

    # API endpoints
    API_BASE = "https://hr-analytics-dashboard.onrender.com"

    # Load KPI Summary
    kpi_data = requests.get(f"{API_BASE}/kpi-summary").json()

    # Header Metrics
    st.title("HR Dashboard")
    col1, col2, col3 = st.columns(3)
    col1.metric("Headcount", kpi_data['headcount'])
    col2.metric("Avg Tenure", kpi_data['avg_tenure'])
    col3.metric("Avg Age", kpi_data['avg_age'])

    # Load Department Summary
    dept_data = pd.DataFrame(requests.get(f"{API_BASE}/departments").json())

    # Bar + Line Combo: Headcount vs Avg Income
    fig_combo = px.bar(dept_data, x="department", y="headcount",
                       title="Headcount and Avg Income by Department")
    fig_combo.add_scatter(
        x=dept_data['department'], y=dept_data['avg_income'], name="Avg Income", yaxis="y2")
    fig_combo.update_layout(yaxis2=dict(overlaying='y', side='right'))
    st.plotly_chart(fig_combo, use_container_width=True)

    # Attrition Rate KPIs
    st.subheader("Attrition Rates")
    attrition_all = requests.get(
        f"{API_BASE}/attrition-rate").json()["attrition_rate"]
    attrition_female = requests.get(
        f"{API_BASE}/attrition-rate?gender=Female").json()["attrition_rate"]
    attrition_sales = requests.get(
        f"{API_BASE}/attrition-rate?department=Sales").json()["attrition_rate"]
    attrition_male_rnd = requests.get(
        f"{API_BASE}/attrition-rate?gender=Male&department=Research%20%26%20Development").json()["attrition_rate"]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total", f"{attrition_all}%")
    col2.metric("Female", f"{attrition_female}%")
    col3.metric("Sales", f"{attrition_sales}%")
    col4.metric("Male in R&D", f"{attrition_male_rnd}%")

    # Load & Display Employees Table
    st.subheader("Employee Data")
    employees = pd.DataFrame(requests.get(
        f"{API_BASE}/employees?limit=2000").json())
    st.dataframe(employees, use_container_width=True)

    # Bar Charts
    st.subheader("Distributions")
    col1, col2 = st.columns(2)

    fig1 = px.histogram(employees, x="department", color="attrition",
                        barmode="group", title="Attrition by Department")
    col1.plotly_chart(fig1, use_container_width=True)

    fig2 = px.histogram(employees, x="department", color="gender",
                        barmode="group", title="Gender by Department")
    col2.plotly_chart(fig2, use_container_width=True)
