FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files (not just app.py)
COPY app.py .
COPY templates ./templates
COPY static ./static

# Environment variables (override at runtime with -e)
ENV FLAG="Bunian{it_W4s_That_simple_4f2a1b}" \
    SECRET_KEY="very_secure_secret" \
    JWT_SECRET="very_secure_jwt"

# Expose the port Flask runs on
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]

