# Use the official Python 3.8 runtime as the parent image
FROM python:3.8-slim

# Set environment variables
ENV DB_URI="mongodb+srv://dishswap.nnokwuw.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
ENV CERT_FILE_PATH="/mongo_cert/X509-cert-7139973848924752117.pem"

# Set the working directory in the container to /app
WORKDIR .

# Copy the current directory contents into the container at /app
COPY . .

# If you have additional dependencies in a requirements.txt file, you can include the next line
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8081
EXPOSE 8081

# Run main.py when the container launches
CMD ["python", "/app/main.py"]
