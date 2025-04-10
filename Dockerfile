FROM python:3.12-slim

# Set environment and working directory
ENV NLTK_DATA=/app/nltk_data
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download punkt to NLTK_DATA
RUN python -m nltk.downloader -d /app/nltk_data punkt

# Copy application files
COPY . .

# Re-declare nltk data path for runtime
ENV NLTK_DATA=/app/nltk_data

# Run the app
CMD ["python", "main.py"]
