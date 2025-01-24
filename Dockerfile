# Use a slim Python base image to keep the image size minimal
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Define a build argument for the application version
ARG APP_VERSION

# Set the application version as an environment variable inside the container
ENV APP_VERSION=${APP_VERSION}

# Add metadata to the container image for version tracking
LABEL version=${APP_VERSION}
LABEL description="Membership Tracker Frontend Service"

# Copy the Python dependencies file into the container
COPY app/requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY app/ .

# Expose the application on port 8000
EXPOSE 8000

# Set the default command to run the FastAPI application using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
