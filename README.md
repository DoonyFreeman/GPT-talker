# GPT Talker

Локальный pet-проект: FastAPI backend принимает промпт, отправляет его в Gemini API, сохраняет историю запросов в SQLite и отдает всё это простому фронтенду в одном файле `index.html`.

## Что делает проект

- Отправляет сообщения в Gemini через `POST /requests`
- Возвращает историю ваших запросов через `GET /requests`
- Сохраняет `prompt/response` в локальную базу `request.db`
- Имеет одностраничный фронтенд без сборки и npm

## Стек

- Python 3.13+
- FastAPI
- Google GenAI SDK
- SQLAlchemy
- SQLite
- HTML/CSS/JS без сборщика

## Скриншоты

Папка под изображения уже подготовлена: `docs/screenshots/`

Рекомендуемые имена файлов:

- `docs/screenshots/chat-main.png` — основной экран чата
- `docs/screenshots/history-panel.png` — боковая панель с историей
- `docs/screenshots/error-state.png` — пример ошибки API

Когда добавите изображения, можно вставить их сюда:

```md
![Main chat](docs/screenshots/chat-main.png)
![History panel](docs/screenshots/history-panel.png)
![Error state](docs/screenshots/error-state.png)
```

## Структура проекта

```text
.
├── config.py           # загрузка конфигурации и .env
├── db.py               # SQLite и модели SQLAlchemy
├── gemini_client.py    # обращение к Gemini API
├── index.html          # фронтенд в одном файле
├── main.py             # FastAPI приложение
├── request.db          # локальная база запросов
├── requirements.txt    # зависимости для pip
└── .env.example        # пример переменных окружения
```

## Как установить зависимости

### Вариант 1. Через `uv`

Требуется установленный `uv`.

```bash
uv sync
```

### Вариант 2. Через `pip`

```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Нужен ли свой API key

Да, если человек просто клонировал этот репозиторий и хочет запустить проект локально у себя, ему нужен **свой Gemini API key**.

Логика здесь простая:

- фронтенд не ходит в Gemini напрямую
- запрос уходит в ваш FastAPI backend
- backend из `gemini_client.py` вызывает Gemini API уже от имени серверной части
- значит, backend должен знать рабочий `GEMINI_API_KEY`

Есть два сценария:

### 1. Пользователь запускает проект локально после `git clone`

В этом случае **да, свой ключ обязателен**. Пользователь должен:

1. Получить Gemini API key у Google
2. Создать `.env` на основе `.env.example`
3. Вставить туда свой ключ
4. Запустить backend

### 2. Пользователь открывает уже развернутый вами сервис

В этом случае **нет, свой ключ ему не нужен**. Ключ хранится у владельца backend, а пользователь просто работает с готовым интерфейсом.

## Как настроить проект у себя

### 1. Подготовьте Gemini API key

Если вы запускаете проект локально у себя, нужен рабочий ключ для Gemini API. Если Google пишет, что ключ помечен как утекший, создайте новый ключ.

### 2. Создайте локальный `.env`

```bash
cp .env.example .env
```

Откройте `.env` и вставьте реальный ключ:

```env
GEMINI_API_KEY=your_real_key_here
```

`config.py` автоматически подхватывает `.env`, поэтому отдельно экспортировать переменную в shell не обязательно.

Если у вас нет своего Gemini API key, backend не сможет отправлять запросы в модель.

### 3. Запустите backend

Если используете `uv`:

```bash
uv run uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Если используете `venv` + `pip`:

```bash
source .venv/bin/activate
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Backend будет доступен по адресу:

```text
http://localhost:8000
```

### 4. Запустите фронтенд

Проекту не нужен отдельный frontend build. Достаточно поднять любой статический сервер в корне проекта.

Простой вариант:

```bash
python3 -m http.server 5000
```

После этого откройте:

```text
http://localhost:5000/index.html
```

## API контракт

### `GET /requests`

Возвращает историю запросов для текущего IP-адреса.

Пример ответа:

```json
[
  {
    "id": 1,
    "ip_address": "127.0.0.1",
    "prompt": "Hello",
    "response": "Hi!"
  }
]
```

### `POST /requests`

Принимает JSON вида:

```json
{
  "prompt": "Explain FastAPI in simple words"
}
```

Пример ответа:

```json
{
  "answer": "FastAPI is a Python framework for building APIs..."
}
```

## Полезные замечания

- История хранится в локальном файле `request.db`
- Фронтенд уже настроен на `http://localhost:8000`
- Для локальной разработки CORS на backend разрешен широко, чтобы браузер не ломал `OPTIONS /requests`
- Пустой промпт backend отклоняет с `400`
- Если Gemini API недоступен, backend возвращает понятный `detail` в ошибке

## Частые проблемы

### `OPTIONS /requests 400 Bad Request`

Обычно это старый процесс FastAPI. Полностью перезапустите backend после изменения CORS-настроек.

### `GEMINI_API_KEY is not configured`

Проверьте, что:

- файл `.env` существует в корне проекта
- в нем есть строка `GEMINI_API_KEY=...`
- backend был перезапущен после изменения `.env`

### `Gemini rejected the API key because it is marked as leaked`

Текущий ключ больше нельзя использовать. Создайте новый и замените его в `.env`.
