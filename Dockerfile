# Use official Python 3.11 slim image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app code
COPY . .

# Expose port 8080 (optional, for documentation)
EXPOSE 8080

# Run the app using Python (main.py already handles PORT)
CMD ["python", "main.py"]
