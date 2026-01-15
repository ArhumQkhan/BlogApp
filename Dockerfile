# Use official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /BlogApp

# Install system dependencies required for Pillow and others
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    libpq-dev \
    sqlite3 \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    libtiff-dev \
    libfreetype6-dev \
    libwebp-dev \
    && rm -rf /var/lib/apt/lists/*



# Copy requirements and install
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Create non-root user
RUN adduser --disabled-password appuser
USER appuser

# Expose Django port
EXPOSE 8001

# Run Django server
CMD ["gunicorn", "BlogProject.wsgi:application", "--bind", "0.0.0.0:8001", "--workers", "3", "--access-logfile", "-", "--error-logfile", "-"]
