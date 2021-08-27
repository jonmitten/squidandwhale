# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
# take all the files located in the current directory and cpy them to the image
COPY . .
# now, all we hve to do is to tell Docker what command we want to run when our image is executed instide a container.
# with CMD
# note that we need to make the application externally visible (i.e. from outside the container) by
# specifying `--host=0.0.0.0`
CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0"]
# python-docker
# |____ app.py
# |____ requirements.txt
# |____ Dockerfile