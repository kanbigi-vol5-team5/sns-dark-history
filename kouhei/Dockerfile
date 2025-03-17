# Dockerfile
FROM python:3.11-slim

WORKDIR /kouhei

# 必要なライブラリをインストール
RUN pip install --no-cache-dir pandas snscrape urllib3

# スクリプトをコピー
COPY ./kouhei.py /kouhei/kouhei.py 

CMD ["python", "/kouhei/kouhei.py","@rokuosan_dev","7"]
