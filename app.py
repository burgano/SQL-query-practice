import random
import sqlite3
import threading
import webbrowser

from flask import Flask, jsonify, redirect, render_template, request, session, url_for

from database import get_tables_data, init_db, reset_db
from exercises import EXERCISES, get_exercises_for_tables

app = Flask(__name__)
app.secret_key = 'sql-trainer-2024-xK9pL'


# ──────────────────────────────────────────────
# Routes
# ──────────────────────────────────────────────

@app.route('/')
def welcome():
    counts = {i: len(get_exercises_for_tables(i)) for i in range(1, 6)}
    return render_template('welcome.html', exercise_counts=counts)


@app.route('/start', methods=['POST'])
def start():
    name = request.form.get('name', '').strip()
    try:
        table_count = max(1, min(5, int(request.form.get('table_count', 1))))
    except ValueError:
        table_count = 1
    dialect = request.form.get('dialect', 'sqlite')
    if dialect not in ('sqlite', 'mysql', 'postgresql'):
        dialect = 'sqlite'
    order_mode = request.form.get('order_mode', 'sequential')
    if order_mode not in ('sequential', 'random'):
        order_mode = 'sequential'

    if not name:
        return redirect(url_for('welcome'))

    available = get_exercises_for_tables(table_count)
    exercise_ids = [e['id'] for e in available]
    if order_mode == 'random':
        random.shuffle(exercise_ids)

    session.clear()
    session['name'] = name
    session['table_count'] = table_count
    session['dialect'] = dialect
    session['order_mode'] = order_mode
    session['exercise_index'] = 0
    session['exercise_ids'] = exercise_ids
    session['score'] = {'correct': 0, 'total': 0, 'revealed': 0}

    init_db()
    return redirect(url_for('trainer'))


@app.route('/trainer')
def trainer():
    if 'name' not in session:
        return redirect(url_for('welcome'))

    name = session['name']
    table_count = session['table_count']
    dialect = session.get('dialect', 'sqlite')
    idx = session.get('exercise_index', 0)
    exercise_ids = session.get('exercise_ids', [])
    score = session.get('score', {'correct': 0, 'total': 0, 'revealed': 0})

    if idx >= len(exercise_ids):
        return render_template('complete.html', name=name, score=score, total=len(exercise_ids))

    exercise = _apply_dialect(EXERCISES[exercise_ids[idx]], dialect)

    # Refresh DB before DML exercises so each attempt starts clean
    if exercise.get('needs_reset', False):
        reset_db()

    tables_data = get_tables_data(table_count)

    return render_template(
        'trainer.html',
        name=name,
        table_count=table_count,
        dialect=dialect,
        tables_data=tables_data,
        exercise=exercise,
        exercise_index=idx + 1,
        total_exercises=len(exercise_ids),
        score=score,
    )


@app.route('/check', methods=['POST'])
def check():
    if 'name' not in session:
        return jsonify({'error': 'Session expired'}), 400

    data = request.get_json()
    user_query = (data.get('query') or '').strip()
    exercise_id = data.get('exercise_id')

    if not user_query:
        return jsonify({'correct': False, 'error': 'Query is empty'})
    if exercise_id not in EXERCISES:
        return jsonify({'correct': False, 'error': 'Invalid exercise ID'})

    dialect = session.get('dialect', 'sqlite')
    exercise = _apply_dialect(EXERCISES[exercise_id], dialect)
    result = _check_answer(user_query, exercise)

    if result.get('correct'):
        scored_ids = set(session.get('scored_ids', []))
        if exercise_id not in scored_ids:
            score = session.get('score', {'correct': 0, 'total': 0, 'revealed': 0})
            score['correct'] += 1
            session['score'] = score
            scored_ids.add(exercise_id)
            session['scored_ids'] = list(scored_ids)
        session.modified = True

    return jsonify(result)


@app.route('/next', methods=['POST'])
def next_exercise():
    if 'name' not in session:
        return jsonify({'error': 'Session expired'}), 400
    session['exercise_index'] = session.get('exercise_index', 0) + 1
    session.modified = True
    return jsonify({'ok': True})


@app.route('/show-answer', methods=['POST'])
def show_answer():
    if 'name' not in session:
        return jsonify({'error': 'Session expired'}), 400

    data = request.get_json()
    exercise_id = data.get('exercise_id')
    if exercise_id not in EXERCISES:
        return jsonify({'error': 'Invalid exercise'}), 400

    dialect = session.get('dialect', 'sqlite')
    exercise = _apply_dialect(EXERCISES[exercise_id], dialect)
    if exercise.get('needs_reset', False):
        reset_db()

    score = session.get('score', {'correct': 0, 'total': 0, 'revealed': 0})
    score['revealed'] += 1
    session['score'] = score
    session.modified = True

    return jsonify({'solution': exercise['solution']})


@app.route('/reset-db', methods=['POST'])
def reset_database():
    reset_db()
    return jsonify({'ok': True})


# ──────────────────────────────────────────────
# Answer checking logic
# ──────────────────────────────────────────────

def _apply_dialect(exercise: dict, dialect: str) -> dict:
    """Return exercise with dialect-specific solution/hint merged in."""
    variants = exercise.get('dialect_variants', {})
    variant = variants.get(dialect)
    if not variant:
        return exercise
    merged = dict(exercise)
    merged.update(variant)
    return merged


_DANGEROUS = ['DROP ', 'TRUNCATE ', 'PRAGMA ', 'ATTACH ', 'DETACH ',
              'CREATE TABLE', 'ALTER TABLE', 'CREATE DATABASE']


def _check_answer(user_query: str, exercise: dict) -> dict:
    q_upper = user_query.upper()
    category = exercise['category']

    # Block destructive commands
    for kw in _DANGEROUS:
        if kw in q_upper:
            return {'correct': False, 'error': f'Command not allowed in the trainer: {kw.strip()}'}

    is_dml = exercise.get('needs_reset', False)

    if is_dml:
        dml_type = exercise['solution'].split()[0].upper()  # INSERT / UPDATE / DELETE
        if not q_upper.lstrip().startswith(dml_type):
            return {'correct': False, 'error': f'This exercise requires a {dml_type} query'}
    else:
        if not q_upper.lstrip().startswith('SELECT'):
            return {'correct': False, 'error': 'This exercise requires a SELECT query'}

    from database import get_connection
    conn = get_connection()
    try:
        if is_dml:
            reset_db()
            conn = get_connection()
            conn.execute(user_query)
            conn.commit()
            row = conn.execute(exercise['verify_query']).fetchone()
            actual = row[0] if row else 0
            correct = (actual == exercise['verify_expected_count'])
            return {'correct': correct}
        else:
            user_rows = conn.execute(user_query).fetchall()
            expected_rows = conn.execute(exercise['solution']).fetchall()
            correct = _compare(user_rows, expected_rows, exercise.get('check_order', False))
            return {'correct': correct}

    except sqlite3.Error as e:
        return {'correct': False, 'error': str(e)}
    finally:
        conn.close()


def _compare(user_rows, expected_rows, check_order: bool) -> bool:
    def norm(rows):
        return [tuple('__NULL__' if v is None else str(v) for v in row) for row in rows]

    u = norm(user_rows)
    e = norm(expected_rows)
    return u == e if check_order else sorted(u) == sorted(e)


# ──────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────

if __name__ == '__main__':
    def _open():
        import time
        time.sleep(1.2)
        webbrowser.open('http://127.0.0.1:5000')

    threading.Thread(target=_open, daemon=True).start()
    app.run(debug=False, port=5000)
