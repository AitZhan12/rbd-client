### qonys-service

FastAPI backend, читающий данные из таблицы `apartments` (заполняется scraper'ом rbd).

```
core/config.py         # настройки (DATABASE_URL, CORS, ...)
db/session.py           # async SQLAlchemy engine/session
models/apartment.py      # ORM-модель apartments
schemas/apartment.py     # pydantic-схемы ответа
api/
  router.py              # корневой роутер, подключает версии API
  v1/
    router.py             # роутер v1, подключает эндпоинты
    endpoints/
      health.py
      apartments.py
main.py                 # создание FastAPI app
```

### Запуск

Используется общий `.venv` проекта rbd (в корне репозитория, зависимости — в корневом `requirements.txt`).

```bash
source ../.venv/bin/activate
cp .env.example .env   # указать DATABASE_URL

cd qonys-service
uvicorn main:app --reload
```

Документация: http://localhost:8000/docs
