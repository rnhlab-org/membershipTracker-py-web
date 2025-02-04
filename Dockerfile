# Use a slim Python base image to keep the image size minimal
FROM python:3.9-slim

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
  CMD ["curl", "--fail", "http://localhost:8000/healthz"]

# Create a non-root user ##Checkov fix
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set the working directory in the container  ##Checkov fix
WORKDIR /app

# Copy the Python dependencies file into the container
COPY app/requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Change ownership ##Checkov fix
COPY app/ ./
RUN chown -R appuser:appuser /app

# Switch to non-root user ##Checkov fix
USER appuser

# Define a build argument for the application version ##Checkov fix
ARG APP_VERSION

# Set the application version as an environment variable inside the container
ENV APP_VERSION=${APP_VERSION}

# Add metadata to the container image for version tracking
LABEL version=${APP_VERSION}
LABEL description="Membership Tracker Frontend Service"

# Copy the application code into the container
COPY app/ .

# Expose the application on port 8000
EXPOSE 8000

# Set the default command to run the FastAPI application using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
