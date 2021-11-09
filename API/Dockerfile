FROM python:3.9
LABEL emale="mountainrabbit01@gmail.com"
LABEL name="BK"

#RUN apt-get update -y
#RUN apt-get install -y python-pip python-dev build-essential
#RUN apt-get update && apt-get install -y locales

#Set locales for korean
#RUN locale-gen ko_KR.UTF-8
#ENV LC_ALL=ko_KR.UTF-8
#ENV LANG=ko_KR.UTF-8
#ENV LANGUAGE=ko_KR.UTF-8
#RUN update-locale LANG=ko_KR.UTF-8
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "./app.py"]
