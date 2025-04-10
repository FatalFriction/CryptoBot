#!/bin/bash
echo "Downloading NLTK punkt tokenizer..."
python3 -m nltk.downloader punkt
echo "Starting the bot..."
python3 main.py