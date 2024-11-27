# Use the official Python image from Docker Hub as a base image
FROM python:3.13-slim

# Set environment variables to avoid Python writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /ground_water_level_prediction/server

# Copy the requirements.txt file into the container
COPY requirements.txt /ground_water_level_prediction/

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r /ground_water_level_prediction/requirements.txt

# Copy the rest of the application code into the container
COPY . /ground_water_level_prediction/server/

# Expose the port that FastAPI will run on (default 8000)
EXPOSE 8000

# Start the FastAPI application using Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

