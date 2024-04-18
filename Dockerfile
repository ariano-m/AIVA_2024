FROM python:3.10

RUN mkdir ./maderas
WORKDIR ./maderas

COPY requirements.txt .
COPY README.md .

RUN mkdir -p ./maderas/server
COPY bin/server/system ./maderas/server

RUN mkdir -p ./maderas/models/Yolo_Training2
COPY bin/server/models/Yolo_Training2 ./maderas/models/Yolo_Training2

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=0

EXPOSE 5000
ENTRYPOINT ["python", "server/app.py"]