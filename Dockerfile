FROM ubuntu:latest
ENV PYTHONUNBUFFERED=1
RUN apt-get update
RUN apt-get install python3 python3-pip -y
WORKDIR /box4bet
COPY . /box4bet/
RUN pip install -r requirements.txt 
