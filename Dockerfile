# Use Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy everything into the container
COPY . .

# Ensure the instance folder exists and copy db
RUN mkdir -p instance
COPY instance/tawasol.db instance/tawasol.db

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Start Flask app with the existing database
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
