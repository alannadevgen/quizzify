# Basic Python image with FastAPI and Uvicorn
FROM python:3.11

# Set the working directory to /app
ENV WORKDIR=/app
WORKDIR $WORKDIR

# Copy only the requirements file to the container
COPY ./requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the entire source code to the container
COPY src/ $WORKDIR/quizzify
COPY .env $WORKDIR

# Set the working directory to /app/quizzify
WORKDIR $WORKDIR/quizzify

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run app.py when the container launches
CMD uvicorn main:app --reload --host 0.0.0.0 --port 8000 --log-config logging.conf
