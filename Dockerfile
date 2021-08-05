FROM python:3.8.11-buster

LABEL Michael Zazula = "m.zazula@gmail.com"

COPY ./requirements.txt /requirements.txt

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y ffmpeg

COPY ./src/ /

RUN pwd

RUN /bin/ls

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]