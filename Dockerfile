FROM python:3.10

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

RUN mkdir ./maderas
WORKDIR ./maderas

COPY requirements.txt .
COPY README.md .

RUN mkdir -p ./server/system
COPY bin/server/system ./server/system

RUN mkdir -p ./models/models
COPY bin/server/models/Yolo_Training2 ./server/models/Yolo_Training2

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV FLASK_APP=main.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=0

WORKDIR ./server/system

EXPOSE 5005
ENTRYPOINT ["python", "main.py"]