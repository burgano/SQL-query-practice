# SQL Query Practice Trainer

An interactive SQL trainer that runs locally in your browser. Practice real queries on a real database — no cloud, no sign-up.

![Welcome page](assets/screenshot-welcome.png)

![Trainer page](assets/screenshot-trainer.png)

## Quick Start

**Requirements:** Python 3.8+ ([python.org](https://www.python.org/downloads/))

```bash
git clone https://github.com/YOUR_USERNAME/sql-query-practice.git
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

The script automatically creates a virtual environment, installs dependencies, and starts the server. The browser will open at `http://127.0.0.1:5000`.

To stop the server — click the **■ Stop server** button on any page of the app.

> **"Port 5000 is in use" error?**
> Kill the process occupying the port:
> ```bash
> # macOS / Linux
> lsof -ti:5000 | xargs kill -9
>
> # Windows
> netstat -ano | findstr :5000
> taskkill /PID <PID_from_above> /F
> ```
> On macOS, port 5000 may be used by AirPlay Receiver — disable it in **System Settings → General → AirDrop & Handoff → AirPlay Receiver**.

## What's Inside

**5 related tables** with realistic data:

| # | Table | Description |
|---|-------|-------------|
| 1 | `users` | 25 users from different cities |
| 2 | `orders` | 40 orders referencing users |
| 3 | `products` | 20 products across categories |
| 4 | `returns` | 12 returns referencing orders |
| 5 | `service_requests` | 18 support tickets |

**130 exercises** across all core SQL topics:

- `SELECT / WHERE / ORDER BY / LIMIT` — 10 exercises
- Filtering: `AND / OR / IN / NOT IN / LIKE / BETWEEN / IS NULL` — 10
- Aggregates: `COUNT / SUM / AVG / MIN / MAX` — 10
- `GROUP BY / HAVING` — 10
- `JOIN / LEFT JOIN` — 10
- Functions: `ROUND / COALESCE / LOWER / ||` — 10
- `CASE WHEN` — 10
- Subqueries — 10
- `INSERT / UPDATE / DELETE` — 10
- Extended JOINs (triple, quadruple, quintuple table joins) — 40

## Features

- **SQL dialect selector** — SQLite, MySQL, or PostgreSQL syntax
- **Exercise order** — sequential (simple → complex) or random
- **Table count** — choose 1–5 tables to control exercise difficulty
- **Hint system** — category hint hidden behind a toggle button
- **Reveal answer** — show the correct solution on demand
- **Answer checking** — compares actual query results, not strings
- **DML exercises** — data is automatically reset before each INSERT/UPDATE/DELETE check

## How It Works

1. Enter your name, choose SQL dialect, exercise order, and number of tables
2. Table data is shown in a sticky panel at the top
3. Write your SQL query in the editor with syntax highlighting
4. Click **Check Result** — your query runs against the real database and results are compared
5. Correct answer → confetti + auto-advance to the next exercise in 1 second

## Stack

- **Python 3.8+** + **Flask** — web server
- **SQLite** — embedded database, no installation needed
- **CodeMirror** — SQL syntax highlighting in the editor
- Vanilla JS + CSS — no frontend frameworks

## Project Structure

```
sql-query-practice/
├── app.py          # Flask routes and answer-checking logic
├── database.py     # Database schema and seed data
├── exercises.py    # 130 exercises with solutions
├── run.sh          # One-command startup (macOS / Linux)
├── run.bat         # One-command startup (Windows)
├── assets/         # Screenshots for README
├── static/
│   ├── style.css
│   └── script.js
└── templates/
    ├── welcome.html
    ├── trainer.html
    └── complete.html
```
