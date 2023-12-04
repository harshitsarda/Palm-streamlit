# Use the official Google Cloud SDK image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your Streamlit app will run on (replace with the appropriate port)
EXPOSE 8080

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["streamlit", "run", "Palm.py", "--server.port=8080", "--server.enableCORS=false"]
