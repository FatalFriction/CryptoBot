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

# Download punkt using default NLTK path
RUN python -c "import nltk; nltk.download('punkt')"

# Copy project files
COPY . .

# Run the script
CMD ["python", "main.py"]
