FROM resin/rpi-raspbian:latest
MAINTAINER robe16

# Port number to listen on
ARG portApplication

# Update
RUN apt-get update && apt-get install -y python python-pip

WORKDIR /HomeControl/server

# Bundle app source
COPY src /HomeControl/server

# Copy app dependencies
COPY req.txt requirements.txt

# Install app dependencies
RUN pip install -r requirements.txt

# Expose the application port and run application
EXPOSE ${portApplication}
CMD python /src/start.py ${portApplication}
