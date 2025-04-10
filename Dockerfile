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
RUN mkdir -p /app/nltk_data && \
    python -c "import nltk; nltk.download('punkt', download_dir='/app/nltk_data')"

# Copy project files
COPY . .

# Run the script
CMD ["python", "main.py"]
