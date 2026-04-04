# SQL Query Practice Trainer

Интерактивный тренажёр SQL-запросов в браузере. Запускается локально одной командой.

## Быстрый старт

```bash
git clone https://github.com/YOUR_USERNAME/sql-query-practice.git
cd sql-query-practice
pip install -r requirements.txt
python app.py
```

Браузер откроется автоматически на `http://127.0.0.1:5000`

## Что внутри

**5 связанных таблиц** с реалистичными данными:

| # | Таблица | Описание |
|---|---------|----------|
| 1 | `users` | 25 пользователей из разных городов |
| 2 | `orders` | 40 заказов, ссылаются на users |
| 3 | `products` | 20 товаров по категориям |
| 4 | `returns` | 12 возвратов, ссылаются на orders |
| 5 | `service_requests` | 18 обращений в поддержку |

**90 заданий** по всем основным операторам SQL:

- `SELECT / WHERE / ORDER BY / LIMIT` — 10 заданий
- Фильтрация: `AND / OR / IN / NOT IN / LIKE / BETWEEN / IS NULL` — 10
- Агрегаты: `COUNT / SUM / AVG / MIN / MAX` — 10
- `GROUP BY / HAVING` — 10
- `JOIN / LEFT JOIN` — 10
- Функции: `ROUND / COALESCE / LOWER / ||` — 10
- `CASE WHEN` — 10
- Подзапросы — 10
- `INSERT / UPDATE / DELETE` — 10

## Как работает

1. На стартовой странице вводишь имя и выбираешь количество таблиц (1–5)
2. Таблицы с данными зафиксированы в верхней части экрана
3. Под ними — задание и поле для ввода SQL с подсветкой синтаксиса
4. Нажимаешь «Проверить результат» — сравниваются реальные результаты запросов
5. Если ответ неверный — можно посмотреть правильный ответ
6. Для DML-заданий (INSERT/UPDATE/DELETE) данные автоматически сбрасываются перед каждой проверкой

## Стек

- **Python 3.8+** + **Flask** — веб-сервер
- **SQLite** — встроенная БД, не требует установки
- **CodeMirror** — подсветка SQL в редакторе
- Vanilla JS + CSS — без фреймворков

## Структура проекта

```
sql-query-practice/
├── app.py          # Flask маршруты и логика проверки
├── database.py     # Схема БД и генерация данных
├── exercises.py    # 90 заданий с решениями
├── static/
│   ├── style.css
│   └── script.js
└── templates/
    ├── welcome.html
    ├── trainer.html
    └── complete.html
```
