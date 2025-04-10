# Use a slim Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy only requirements first to cache better
COPY requirements.txt .

# Install system dependencies and Python dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && pip install -r requirements.txt

# Download NLTK punkt tokenizer at build time
RUN python -m nltk.downloader -d /app/nltk_data punkt

# Copy app code
COPY . .

# Set env so NLTK knows where to look
ENV NLTK_DATA=/app/nltk_data

# Start the app
CMD ["python", "main.py"]
