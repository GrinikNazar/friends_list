FROM python:3.11-slim

WORKDIR /bot

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot/ .

CMD ["python", "bot.py"]