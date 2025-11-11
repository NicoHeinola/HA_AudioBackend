FROM python:3.12-slim

WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy application code
COPY . .

# Default command
CMD ["python", "main.py"]
