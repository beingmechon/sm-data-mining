# Use Python 3.8 slim version as base image
FROM python:3.8-slim

# Set working directory in the container
WORKDIR /app

# Copy the entire project directory contents into the container at /app
COPY . /app

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install ChromeDriver
RUN apt-get update && apt-get install -y wget unzip && \
    wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/91.0.4472.101/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver

# Create necessary directories
RUN mkdir -p /app/logs /app/data/comments /app/data/cluster_summary /app/data/clusters

# Set the command to run the main.py script when the container starts
CMD ["python", "main.py"]
