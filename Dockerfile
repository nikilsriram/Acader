FROM python:3.9-slim

WORKDIR /app

# Cleaned up dependencies - removed the broken package
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy your requirements file and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all your project files
COPY . .

# Expose the default Streamlit port
EXPOSE 8501

# Run your main dashboard file
CMD ["streamlit", "run", "dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
