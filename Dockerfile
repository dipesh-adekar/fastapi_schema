FROM python:3.10

RUN apt update

RUN useradd -ms /bin/bash testuser
USER testuser

WORKDIR /home/testuser/code

COPY --chown=testuser:testuser requirements.txt .
RUN pip install --user -r requirements.txt  

COPY --chown=testuser:testuser . .

ENV PYTHONUNBUFFERED=1

EXPOSE 8000