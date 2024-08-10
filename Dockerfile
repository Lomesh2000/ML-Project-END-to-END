FROM python:3.8-slim

WORKDIR /app

COPY . /app

# RUN set -xe \
#     && apk update update -y \
#     && apk update install -y python3-pip

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", 'app.py' ]

