# HR Analytics Dashboard

A full-stack HR analytics dashboard for visualizing employee data and attrition metrics. Built using FastAPI, PostgreSQL, and Streamlit, the project features scheduled ETL workflows, a modular API, and an interactive frontend.


Live Links
- Backend live API: [HR analytics dashboard API](https://hr-analytics-dashboard.onrender.com/)
- Streamlit dashboard: [HR Dashboard](https://hr-dashboard-3q51.onrender.com/)

---


![Dashboard Preview](assets/dashboard-preview.png)

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Setup & Installation](#setup--installation)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Create a Virtual Environment](#2-create-a-virtual-environment)
  - [3. Install Dependencies](#3-install-dependencies)
  - [4. Environment Variables](#4-environment-variables)
  - [5. Populate the Database (Optional for Template)](#5-populate-the-database-optional-for-template)
  - [6. Run Locally](#6-run-locally)
- [Deployment](#deployment)
- [Authentication (Optional)](#authentication-optional)
- [Agile Process & Kanban](#agile-process--kanban)
- [Responsive Design](#responsive-design)

---

## Overview

This project is a modular, ready-to-deploy HR dashboard. It’s built as a template to adapt to new datasets. Simply change the `.csv` file or database and the visuals will adjust dynamically.

---

## Features

- KPI Summary: Headcount, Average Age, Tenure
- Department Breakdown: Headcount + Income
- Attrition Insights: Overall & filtered by gender/department
- Employee Table: Full dataset browser
- Streamlit UI: Modern, responsive, & interactive
- ETL Workflow: Converts CSV to normalized database
- Modular API: Built with FastAPI
- Deployment Ready: Dockerized + Render-ready
- Authentication: Streamlit Authenticator (optional)

---


## Tech Stack

- **Backend**: FastAPI + SQLAlchemy + PostgreSQL (Neon)
- **Frontend**: Streamlit + Plotly
- **ETL**: Pandas + GitHub Actions (cron + manual)
- **Auth**: Optional (Streamlit Authenticator)
- **Deployment**: Render (Dockerized)

---

## Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/MilenTecle/hr-analytics-dashboard.git
cd hr-analytics-dashboard
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Variables

Create a `.env` file based on the included `.env.template`. Required:

```env
DATABASE_URL=postgresql://your_user:your_pass@your_host/your_db
IS_TEMPLATE=false
```

### 5. Populate the Database (Optional for Template)

```bash
$env:IS_TEMPLATE = "false"
python etl/run_etl.py
```

- The ETL reads from a fallback `.example.csv` only if IS_TEMPLATE=true
- Private datasets are not committed for security
- Dashboards adapt to any HR CSV matching the required schema
- Switch `IS_TEMPLATE=false` to load real dataset


### 6. Run Locally

**Run the backend (FastAPI):**

```bash
uvicorn hr_api.main:app --reload
```

**Run the frontend (Streamlit):**

```bash
streamlit run streamlit_app.py
```

---

## Deployment

The project includes:

- `Dockerfile` for Streamlit app
- `render.yaml` for Render deployment

Steps:

1. Push repo to GitHub
2. Link repo on Render
3. Add a new Web Service
4. Select Docker and set build command to auto
5. Set environment variables: `DATABASE_URL`, `IS_TEMPLATE`
6. Done!

---

## Authentication (Optional)

Authentication is disabled for demo purposes to allow public access to the dashboard.
This template supports Streamlit Authenticator.
Uncomment the relevant code and define credentials to restrict access.

```python
# streamlit_app.py

from streamlit_authenticator import Authenticate
```

See [streamlit-authenticator](https://github.com/mkhorasani/streamlit-authenticator) for setup.

---


## Agile Process & Kanban

- Project tracked using GitHub Projects (Kanban) → [View Board](https://github.com/MilenTecle/hr-analytics-dashboard/projects)

- Commits reference story progress

---

## Responsive Design

The dashboard is designed to render seamlessly across:

- Desktop
- Tablets
- Mobile

Dark mode is default.

---

Built by Milen Tecle