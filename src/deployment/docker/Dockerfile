# Use a lightweight Python image as the base
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV MODEL_PATH=/src/models/saved_model
ENV DATA_PATH=/data/processed

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code into the container
COPY ../.. /app

# Expose the port the app runs on
EXPOSE 5000

# Command to run the API server (adjust based on your app)
# If using FastAPI:
CMD ["uvicorn", "src.deployment.api:app", "--host", "0.0.0.0", "--port", "5000"]
# If using Flask, uncomment the line below and comment out the FastAPI line
# CMD ["python", "src/deployment/api.py"]
