# Dockerfile for a Python application
# Using a slim version of Python 3.13 as the base image
FROM python:3.13-slim

# Set the working directory in the container
# This is where the application code will be copied
WORKDIR /app

# Copy the application code and requirements file into the container
# The requirements.txt file is used to install the necessary Python packages
COPY . /app

# Install the required Python packages
# Using --no-cache-dir to avoid caching the packages, reducing image size
RUN pip install --no-cache-dir -r requirements.txt

#Create volume for persistent data
VOLUME [ "/app/logs", "/app/data" ]

# Expose ports for the application
# Port 22 for SSH, port 80 for HTTP, and port 21 for FTP
EXPOSE 22 80 21

# Add a non-root user to run the application
# This enhances security by not running the application as the root user
RUN useradd -ms /bin/bash honeypotuser
USER honeypotuser

# Command to run the application
# This will start the application using the Python interpreter
CMD ["python", "honeypot/main.py"]