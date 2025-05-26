# Start from the official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies, including git
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy rest of the app
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Run Streamlit app
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.enableCORS=false"]