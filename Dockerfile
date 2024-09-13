FROM python:3-alpine3.10

WORKDIR /app
COPY . .


RUN pip install --upgrade pip
RUN apk add ffmpeg
RUN pip install -r requirements.txt

EXPOSE 6969

CMD ["python3", "./app.py"]