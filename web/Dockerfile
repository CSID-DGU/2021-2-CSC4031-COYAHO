FROM python:3.9
LABEL email="mountainrabbit01@gmail.com"
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "./app.py"]