# Use Python 3.13.1 base image
FROM python:3.13.1-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Ensure logs are shown in real-time
ENV PYTHONUNBUFFERED=1

# Start the service
CMD ["python", "main.py"]
