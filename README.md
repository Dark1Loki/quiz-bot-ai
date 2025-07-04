# Telegram Quiz Bot на тему "Разработка ИИ"

Этот бот создан для самоконтроля знаний по теме "Разработка искусственного интеллекта (ИИ)". Пользователь проходит тест, отвечает на вопросы и получает финальную статистику.

---

## 📦 Возможности

- Команда `/start` — приветствие и запуск.
- Кнопка **"Начать игру"** — старт квиза.
- Вопросы с вариантами ответа (инлайн-кнопки).
- Ответы отображаются в чате.
- Подсчёт правильных ответов.
- Финальная статистика (кол-во правильных, %).
- Хранение прогресса в SQLite-базе.

---

## 🚀 Как запустить

1. Установите зависимости:
   ```bash
   pip install aiogram aiosqlite
   ```

2. Укажите токен бота в `bot.py`:
   ```python
   API_TOKEN = 'ВАШ_ТОКЕН_ОТ_BOTFATHER'
   ```

3. Запустите бота:
   ```bash
   python bot.py
   ```

---

## 📁 Структура проекта

```
quiz_bot/
├── bot.py                   # Точка входа
├── handlers/
│   ├── start.py             # Команда /start
│   └── quiz.py              # Вопросы и ответы
├── services/
│   ├── db.py                # Работа с SQLite
│   └── quiz_logic.py        # Генерация вопросов и клавиатуры
├── data/
│   └── questions.py         # Список вопросов
├── quiz_bot.db              # База данных (создаётся автоматически)
└── README.md                # Документация проекта
```

---

## ❓ Пример вопроса

> ❓ Какой язык чаще всего используется для создания моделей ИИ?

```
🔘 Python
🔘 C++
🔘 HTML
🔘 Java
```

---

## 📊 Пример результата

> Квиз завершён!  
> Ваш результат: **8/10** правильных ответов (**80%**)

---

## 👨‍💻 Автор

Telegram Quiz Bot создан в рамках учебного задания по Python и Telegram Bot API.
