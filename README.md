# 🧑‍🤝Friends API + Telegram Bot

Цей проєкт складається з:
- **FastAPI бекенду**, який дозволяє створювати, переглядати та отримувати друзів;
- **Telegram-бота** (на `pytelegrambotapi`), який працює з тим самим бекендом;
- **Docker-оточення** для зручного запуску;
- **pytest-тестів** для перевірки основних функцій API.

---

## 🚀 Стек технологій

- [FastAPI](https://fastapi.tiangolo.com/)
- [Python 3.11.5](https://www.python.org/)
- [PyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
- [AWS S3 / DynamoDB](https://aws.amazon.com/)
- [Docker & Docker Compose](https://www.docker.com/)
- [pytest](https://pytest.org/)

## ⚙️ Встановлення та локальний запуск

### 1. Клонування репозиторію
```bash
git clone https://github.com/GrinikNazar/friends_list.git
cd friends_list
```

### 2. Створення віртуального оточення
````
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
````
### 3. Встановлення залежностей
```
pip install -r requirements.txt
```

### 4. Створення .env файлу
У корені проекту створіть .env файл
```
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=eu-central-1
BOT_TOKEN=your_telegram_bot_token
```

## ▶️ Запуск локально
🔹 Бекенд
```
uvicorn main:app --reload
```
🔹 Telegram-бот
```
python bot/bot.py
```

## 🧪 Тестування (pytest)

Передбачено базові тести:
- створення друга без обов’язкових полів → 422
- створення друга з валідним фото → 200
- отримання списку друзів → 200

### Запуск тестів:
```
pytest -v
```

## 🐳 Запуск Docker
### Збірка образу
```
docker compose up --build   
```

## 🧩 API Ендпоінти
| Метод  | Ендпоінт        | Опис                   |
| ------ | --------------- | ---------------------- |
| `POST` | `/friends`      | Створити друга         |
| `GET`  | `/friends`      | Отримати список друзів |
| `GET`  | `/friends/{id}` | Отримати друга за ID   |
| `DELETE`| `/friends/{id}`| Видалити друга по ID   |

## 🐳 Запуск Docker на сервері Ubuntu
```
docker-compose build --no-cache
docker-compose up -d
```
### Переглянути запущені контейнери Docker
```
docker ps
```

