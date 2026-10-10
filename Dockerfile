FROM python:3.14-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# --- FIXES FOR GOOGLE SEARCH CRAWLER ---
# 1. Overwrites the raw static template title so Google indexes your brand name
RUN sed -i 's|<title>Streamlit</title>|<title>Acader</title>|' $(python -c "import streamlit; import pathlib; print(pathlib.Path(streamlit.__file__).parent / 'static' / 'index.html')")

# 2. Overwrites the raw noscript warning so Google displays a clean snippet description under your name
RUN sed -i 's|You need to enable JavaScript to run this app.|Acader - Your ultimate study platform for notes, flashcards, and progress tracking.|' $(python -c "import streamlit; import pathlib; print(pathlib.Path(streamlit.__file__).parent / 'static' / 'index.html')")
# --------------------------------------

EXPOSE 8501

CMD ["streamlit", "run", "dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
