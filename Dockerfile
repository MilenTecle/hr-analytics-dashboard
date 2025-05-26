# ---- Base image ----
FROM python:3.10-slim

# ---- Set environment variables ----
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ---- Set working directory ----
WORKDIR /app

# ---- Install system dependencies ----
RUN apt-get update && \
    apt-get install -y build-essential && \
    apt-get clean

# ---- Install Python dependencies ----
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ---- Copy application files ----
COPY . .

# ---- Expose Streamlit port ----
EXPOSE 8501

# ---- Start the app ----
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.enableCORS=false"]