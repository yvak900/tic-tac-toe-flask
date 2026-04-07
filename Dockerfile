# Use lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 5000

# Run app using gunicorn (production server)
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:5000", "app:app"]