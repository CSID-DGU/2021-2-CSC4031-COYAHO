FROM ubuntu:18.04
MAINTAINER your_name "email@gmail.com"

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential

#Set locales for korean
RUN apt-get install locales
ENV LC_ALL ko_KR.UTF-8
ENV PYTHONIOENCODING=utf-8

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "./app.py"]
