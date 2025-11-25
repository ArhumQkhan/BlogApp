# Use an official Python runtime as a parent image
FROM python:3.11-slim

# ------------ Set enviroment variables -------------

# Python will run .py files directly without generating .pyc files.
ENV PYTHONDONTWRITEBYTECODE=1
# Python output is sent straight to terminal without buffering.
# By default, Python buffers output (stores it in memory before printing), which can delay logs in Docker.
ENV PYTHONUNBUFFERED=1

# ------------ Set work directory -------------

WORKDIR /BlogApp

# Install system dependencies
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev sqlite3 && \
    rm -rf /var/lib/apt/lists/*


# Copy the rest of the application code
COPY . /BlogApp/

# Create virtual environment inside the container
RUN python3 -m venv /BlogApp/venv

# Set enviroment variable so docker container uses the virtual enviroment
ENV PATH="/BlogApp/venv/bin:$PATH"

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port 8000 for the application (optional, Django default port)
EXPOSE 8000

# Command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]