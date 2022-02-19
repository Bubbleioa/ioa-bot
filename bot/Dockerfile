FROM python:3.10.2-alpine3.15

WORKDIR /usr/src/app

RUN apk update \
    && apk add --virtual build-dependencies build-base gcc \
    && apk add tzdata \
    && apk add zlib-dev jpeg-dev libjpeg freetype-dev \
    && apk add --no-cache libstdc++


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN apk del build-dependencies

COPY . .

CMD [ "python", "bot.py" ]
