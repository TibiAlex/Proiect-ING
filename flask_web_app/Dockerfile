# Base image
FROM python:3.9-slim-buster

# Set working directory
WORKDIR /app

# Copy application files to container
COPY . .

# Install flask
RUN pip3 install flask

# Set env variables
ENV FLASK_APP=flask_app
ENV FLASK_ENV=development

# Expose the necessary port
EXPOSE 5000

# Define the command to start the application
CMD ["flask", "run", "--host=0.0.0.0"]

# By default, when you run the Flask development server using flask run,
# it binds to the loopback interface (127.0.0.1), which means that the server
# can only be accessed from inside the container.
# Adding the --host=0.0.0.0 option to the CMD command allows the Flask server
# to be accessed from outside the container, which is necessary if you want
# to interact with the application from your host machine or from other
# containers on the same network