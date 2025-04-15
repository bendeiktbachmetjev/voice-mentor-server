# 🎙️ Voice Mentor Server

Минимальный сервер для коучинговых советов на основе аудиосообщений (Flask + OpenAI).

## Возможности
- Принимает аудиофайл (.wav) через POST /upload
- Распознаёт речь с помощью OpenAI Whisper API
- Анализирует текст и возвращает короткий коучинговый совет через GPT-3.5-turbo

## Быстрый старт

1. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Экспортируйте ключ OpenAI:**
   ```bash
   export OPENAI_API_KEY=your_openai_key
   ```
3. **Запустите сервер:**
   ```bash
   python server.py
   ```
4. **Отправьте запрос:**
   Пример с помощью `curl`:
   ```bash
   curl -X POST -F "file=@your_audio.wav" http://localhost:5000/upload
   ```

## Структура проекта
```
voice-mentor-server/
├── server.py           # Flask сервер, точка входа
├── whisper_worker.py   # Работа с Whisper API
├── gpt_worker.py       # Работа с GPT API
├── config.py           # Конфиг и переменные окружения
├── requirements.txt    # Зависимости
├── render.yaml         # Конфиг для Render
└── README.md           # Эта инструкция
```

## Переменные окружения
- `OPENAI_API_KEY` — ключ OpenAI (обязателен)

## Для деплоя на Render
- Используйте готовый `render.yaml` и настройте переменные окружения.

---

**Пример запроса:**

Пользователь: «Я не уверен, стоит ли начинать проект.»  
Ответ: «Ты часто говоришь, что не уверен. Попробуй переформулировать: ‘Я хочу разобраться’. Это звучит увереннее.»

---

**Контакты:**
- Вопросы и предложения: [ваш email или телеграм]
