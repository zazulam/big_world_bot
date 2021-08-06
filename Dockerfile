FROM python:3.8.11-buster

LABEL maintainer="m.zazula@gmail.com"

COPY ./requirements.txt /requirements.txt

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y ffmpeg

COPY ./src/ /

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]