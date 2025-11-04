FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libjpeg-dev zlib1g-dev && \
    apt-get clean


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .


EXPOSE 8000


RUN pip install supervisor

RUN echo "[supervisord]\nnodaemon=true\n\
[program:backend]\ncommand=uvicorn app.main:app --host 0.0.0.0 --port 8000\n\
[program:bot]\ncommand=python bot/bot.py\n" > /etc/supervisord.conf

CMD ["supervisord", "-c", "/etc/supervisord.conf"]