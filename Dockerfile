FROM python:3.9-slim

WORKDIR /app

# Install system dependencies required for Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy your requirements file first to take advantage of Docker caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all your project files into the container
COPY . .

# Expose the default port that Streamlit listens on
EXPOSE 8501

# Run your main routing dashboard file when the container starts
CMD ["streamlit", "run", "dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
