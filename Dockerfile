# Use an official Python 3.11 runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /usr/src/app
COPY ./src/ /app/src/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir canopy-sdk pydantic fastapi uvicorn openai

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run app.py when the container launches
CMD ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "8000"]
