from python:3.8-slim-buster


WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip --no-cache-dir install -r requirements.txt

COPY . /app

EXPOSE 5000

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]