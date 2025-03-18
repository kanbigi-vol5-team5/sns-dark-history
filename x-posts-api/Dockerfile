FROM python:3.9

ENV PYTHONIOENCODING utf-8
ENV TZ="Asia/Tokyo"
ENV LANG=C.UTF-8
ENV LANGUAGE=en_US:en_US

WORKDIR /app

COPY ./x-posts-api/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY ./x-posts-api /app/x-posts-api

WORKDIR /app/x-posts-api

CMD ["python3", "main.py"]
