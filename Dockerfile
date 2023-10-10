# Use the official Python 3.9 runtime as the parent image
FROM python:3.9-slim

# Set the working directory in the container to /app
WORKDIR .

# Copy the current directory contents into the container at /app
COPY . .

# If you have additional dependencies in a requirements.txt file, you can include the next line
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8090
EXPOSE 8090

# Run main.py when the container launches
CMD ["python", "/app/main.py"]
