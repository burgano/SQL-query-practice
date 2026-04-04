# SQL Query Practice Trainer

A local SQL trainer that runs in your browser. Practice real queries on a real database, no sign-up, no cloud.

![Welcome page](assets/screenshot-welcome.png)

![Trainer page](assets/screenshot-trainer.png)

## Quick Start

You need Python 3.8+ installed: [python.org](https://www.python.org/downloads/)

```bash
git clone https://github.com/burgano/SQL-query-practice.git
cd sql-query-practice
```

**macOS / Linux:**
```bash
bash run.sh
```

**Windows:**
```bat
run.bat
```

The script creates a virtual environment, installs dependencies and starts the server. Browser will open at `http://127.0.0.1:5000`.

To stop the server use the **Stop server** button inside the app.

> **"Port 5000 is in use" error?**
> Kill the process on that port:
> ```bash
> # macOS / Linux
> lsof -ti:5000 | xargs kill -9
>
> # Windows
> netstat -ano | findstr :5000
> taskkill /PID <PID> /F
> ```
> On macOS port 5000 can be taken by AirPlay Receiver. Disable it in System Settings > General > AirDrop & Handoff > AirPlay Receiver.

## What's Inside

5 related tables with realistic data:

| # | Table | Description |
|---|-------|-------------|
| 1 | `users` | 25 users from different cities |
| 2 | `orders` | 40 orders |
| 3 | `products` | 20 products |
| 4 | `returns` | 12 returns |
| 5 | `service_requests` | 18 support tickets |

130 exercises covering:

- `SELECT / WHERE / ORDER BY / LIMIT`
- `AND / OR / IN / NOT IN / LIKE / BETWEEN / IS NULL`
- `COUNT / SUM / AVG / MIN / MAX`
- `GROUP BY / HAVING`
- `JOIN / LEFT JOIN`
- `ROUND / COALESCE / LOWER / concatenation`
- `CASE WHEN`
- Subqueries
- `INSERT / UPDATE / DELETE`
- Multi-table JOINs (3, 4, 5 tables)

## Features

- Choose SQL dialect: SQLite, MySQL or PostgreSQL
- Sequential or random exercise order
- 1 to 5 tables depending on what you want to practice
- Hint system hidden behind a button
- Reveal answer on demand
- Answer checked by comparing actual query results, not strings
- DML exercises reset the data before each check

## Stack

Python 3.8+ / Flask / SQLite / CodeMirror / Vanilla JS

## Project Structure

```
sql-query-practice/
├── app.py
├── database.py
├── exercises.py
├── run.sh
├── run.bat
├── assets/
├── static/
│   ├── style.css
│   └── script.js
└── templates/
    ├── welcome.html
    ├── trainer.html
    └── complete.html
```
