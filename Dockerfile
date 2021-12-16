FROM rasa/rasa:2.8.16-full

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

USER root

RUN apt update && \
    apt install -y make

RUN pip install black \
    debugpy \
    typedb-client==2.5.0


WORKDIR /app
EXPOSE 5005

