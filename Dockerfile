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

# Download punkt and move it where sumy expects it
RUN python -m nltk.downloader -d $NLTK_DATA punkt \
 && mkdir -p $NLTK_DATA/tokenizers/punkt_tab/english \
 && cp $NLTK_DATA/tokenizers/punkt/english.pickle $NLTK_DATA/tokenizers/punkt_tab/english/english.pickle

# Copy project files
COPY . .

# Expose NLTK path at runtime
ENV NLTK_DATA=/app/nltk_data

# Run the script
CMD ["python", "main.py"]
