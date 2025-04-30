FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set NLTK_DATA environment variable
ENV NLTK_DATA=/app/nltk_data

# Create the nltk_data directory and download punkt into it
RUN python -m nltk.downloader -d $NLTK_DATA punkt && \
    mkdir -p $NLTK_DATA/tokenizers/punkt_tab/english && \
    cp -r $NLTK_DATA/tokenizers/punkt/english/* $NLTK_DATA/tokenizers/punkt_tab/english/ || echo "Punkt data not found; skipping copy"

# Copy project files
COPY . .

# Run the script
CMD ["python", "main.py"]
