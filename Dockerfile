# Use the Debian image
FROM debian:bullseye

# Update and install necessary packages
RUN apt-get update \
    && apt-get install -y \
        # Add any additional packages you need here \
    && rm -rf /var/lib/apt/lists/*

# Switch to Python image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install necessary dependencies
RUN pip install --upgrade pip==20.3.4 \
    && apt-get update \
    && apt-get install -y libgomp1 \
    && pip install numpy \
    && pip install -r requirements.txt

# Command to run your application
CMD ["python", "main.py"]

