# Base image with all necessary system dependencies for Playwright
FROM mcr.microsoft.com/playwright/python:v1.52.0-jammy

# Set work directory
WORKDIR /app

# Copy your code
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Collect static files, migrate DB
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

# Expose the port your app runs on (adjust if not 8000)
EXPOSE 8000

# Start the app
CMD ["gunicorn", "product_scraper.wsgi:application", "--bind", "0.0.0.0:8000", "--timeout", "250", "--workers", "1"]

