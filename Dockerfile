# Use AMD64-compatible lightweight Python image
FROM --platform=linux/amd64 python:3.10-slim

# Set working directory
WORKDIR /app

# Copy all necessary files and folders
COPY main.py .
COPY utils/ utils/
COPY models/ models/
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Ensure input and output directories exist
RUN mkdir -p input output

# Set entry point
CMD ["python", "main.py"]