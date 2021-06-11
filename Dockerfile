FROM ubuntu:latest
ENV PYTHONUNBUFFERED=1
RUN apt-get update
RUN apt-get install python3 python3-pip -y
WORKDIR /box4bet
ADD ./requirements.txt /box4bet
RUN pip install -r requirements.txt
COPY . /box4bet/
CMD ["python3", "manage.py", "runserver", "0.0.0.0:80", "--insecure"]
