FROM python:3.13-slim

# Install system dependencies
RUN apt-get update && apt-get install -y curl build-essential && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

# Copy all project files
COPY . /app

# Configure Poetry and install deps
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Streamlit config
ENV STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_ENABLECORS=false \
    STREAMLIT_SERVER_HEADLESS=true

EXPOSE 8501

# Run the app located inside src/
CMD ["streamlit", "run", "app.py"]
