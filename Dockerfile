# Use official Python image
FROM python:3.11-slim

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

# Copy project files
COPY . /BlogApp/

# Upgrade pip and install dependencies globally
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose Django port
EXPOSE 8001

# Run Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
