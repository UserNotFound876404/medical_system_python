#!/bin/bash
# Install Tesseract OCR on Azure App Service startup

# Update package list
apt-get update

# Install Tesseract + dependencies
apt-get install -y tesseract-ocr tesseract-ocr-eng libtesseract-dev libleptonica-dev

# Verify installation
tesseract --version

# Start your Flask app
gunicorn --bind=0.0.0.0 --timeout 600 server:app
