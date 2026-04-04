import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'trainer.db')

TABLE_ORDER = ['users', 'orders', 'products', 'returns', 'service_requests']

USERS_DATA = [
    (1,  'Anna Smith',       'anna.smith@gmail.com',    28, 'Moscow',           '+7-999-111-1111',   '2023-03-15', 1),
    (2,  'Ivan Petrov',      'ivan.petrov@mail.ru',     35, 'Saint Petersburg',  None,                '2022-07-20', 1),
    (3,  'Maria Garcia',     'maria.garcia@gmail.com',  24, 'Madrid',            '+34-600-222-333',   '2023-11-01', 1),
    (4,  'John Smith',       'john.smith@yahoo.com',    42, 'London',            '+44-700-333-444',   '2021-05-10', 1),
    (5,  'Elena Volkov',     'elena.volkov@mail.ru',    29, 'Moscow',            None,                '2023-08-22', 0),
    (6,  'Pierre Dubois',    'p.dubois@gmail.com',      31, 'Paris',             '+33-600-555-666',   '2022-12-05', 1),
    (7,  'Alice Brown',      'alice.brown@gmail.com',   19, 'London',            '+44-700-777-888',   '2024-01-15', 1),
    (8,  'Dmitry Kozlov',    'dmitry.k@yandex.ru',      45, 'Moscow',            '+7-999-222-3333',   '2021-09-30', 1),
    (9,  'Sophie Martin',    's.martin@gmail.com',      26, 'Paris',             None,                '2023-06-10', 1),
    (10, 'Carlos Lopez',     'carlos.l@hotmail.com',    33, 'Madrid',            '+34-611-999-000',   '2022-04-18', 0),
    (11, 'Olga Novak',       'olga.novak@gmail.com',    22, 'Moscow',            '+7-999-444-5555',   '2024-02-28', 1),
    (12, 'James Wilson',     'j.wilson@yahoo.com',      38, 'New York',          '+1-212-111-2222',   '2021-11-14', 1),
    (13, 'Yuki Tanaka',      'yuki.tanaka@gmail.com',   27, 'Tokyo',             None,                '2023-09-05', 1),
    (14, 'Hannah Mueller',   'h.mueller@gmail.com',     31, 'Berlin',            '+49-170-333-4444',  '2022-06-20', 1),
    (15, 'Artem Sokolov',    'artem.s@mail.ru',         23, 'Saint Petersburg',  '+7-812-555-6666',   '2023-12-10', 1),
    (16, 'Laura Bianchi',    'l.bianchi@gmail.com',     36, 'Paris',             None,                '2022-03-08', 0),
    (17, 'Maxim Fedorov',    'maxim.f@yandex.ru',       41, 'Moscow',            '+7-999-777-8888',   '2021-07-25', 1),
    (18, 'Emma Johnson',     'emma.j@gmail.com',        25, 'London',            '+44-700-444-555',   '2023-05-17', 1),
    (19, 'Pablo Rodrigo',    'pablo.r@gmail.com',       29, 'Madrid',            None,                '2023-10-30', 1),
    (20, 'Natalia Ivanova',  'natalia.i@mail.ru',       34, 'Saint Petersburg',  '+7-812-666-7777',   '2022-01-12', 1),
    (21, 'Tom Anderson',     't.anderson@yahoo.com',    21, 'New York',          '+1-212-222-3333',   '2024-03-01', 1),
    (22, 'Akira Yamamoto',   'akira.y@gmail.com',       28, 'Tokyo',             '+81-90-111-2222',   '2023-07-15', 1),
    (23, 'Ingrid Berg',      'ingrid.b@gmail.com',      44, 'Berlin',            None,                '2021-12-20', 1),
    (24, 'Sergei Morozov',   'sergei.m@yandex.ru',      37, 'Moscow',            '+7-999-888-9999',   '2022-09-03', 0),
    (25, 'Diana Prince',     'diana.p@gmail.com',       30, 'London',            '+44-700-555-666',   '2023-04-22', 1),
]

PRODUCTS_DATA = [
    (1,  'Wireless Mouse',      'Electronics', 29.99,  150, '2022-01-10'),
    (2,  'USB-C Hub',           'Electronics', 49.99,   80, '2022-02-15'),
    (3,  'Mechanical Keyboard', 'Electronics', 119.99,  45, '2022-03-20'),
    (4,  'Python Programming',  'Books',        34.99,  200, '2022-04-01'),
    (5,  'SQL for Beginners',   'Books',        24.99,  180, '2022-05-10'),
    (6,  'Running Shoes',       'Sports',       89.99,   60, '2022-06-15'),
    (7,  'Yoga Mat',            'Sports',       19.99,  100, '2022-07-20'),
    (8,  'Cotton T-Shirt',      'Clothing',     14.99,  300, '2022-08-01'),
    (9,  'Denim Jeans',         'Clothing',     59.99,  120, '2022-09-10'),
    (10, 'LED Desk Lamp',       'Electronics',  39.99,   90, '2022-10-15'),
    (11, 'Bluetooth Speaker',   'Electronics',  79.99,   55, '2022-11-20'),
    (12, 'Coffee Maker',        'Home',         99.99,   40, '2022-12-01'),
    (13, 'Air Purifier',        'Home',        149.99,   25, '2023-01-10'),
    (14, 'Data Science Book',   'Books',        44.99,   90, '2023-02-15'),
    (15, 'Winter Jacket',       'Clothing',    129.99,   35, '2023-03-20'),
    (16, 'Fitness Tracker',     'Electronics',  69.99,    0, '2023-04-01'),
    (17, 'Camping Tent',        'Sports',      199.99,   15, '2023-05-10'),
    (18, 'Ceramic Mug Set',     'Home',         24.99,  200, '2023-06-15'),
    (19, 'Sunglasses',          'Clothing',     39.99,   85, '2023-07-20'),
    (20, 'Smart Doorbell',      'Electronics',  89.99,    0, '2023-08-01'),
]

# (id, user_id, product_id, quantity, total_price, status, ordered_at)
# Users 13, 21, 22, 23 have NO orders (for LEFT JOIN demo)
ORDERS_DATA = [
    (1,  1,  3,  1, 119.99, 'delivered', '2023-04-01'),
    (2,  1,  1,  2,  59.98, 'delivered', '2023-05-15'),
    (3,  2,  5,  1,  24.99, 'delivered', '2023-06-20'),
    (4,  2,  4,  1,  34.99, 'pending',   '2024-01-10'),
    (5,  3,  8,  3,  44.97, 'delivered', '2023-07-05'),
    (6,  3,  9,  1,  59.99, 'cancelled', '2023-08-12'),
    (7,  4, 11,  1,  79.99, 'delivered', '2023-09-01'),
    (8,  4, 12,  1,  99.99, 'delivered', '2023-10-15'),
    (9,  5,  1,  1,  29.99, 'delivered', '2023-11-20'),
    (10, 6, 10,  2,  79.98, 'delivered', '2023-12-01'),
    (11, 7,  6,  1,  89.99, 'pending',   '2024-01-05'),
    (12, 8, 13,  1, 149.99, 'delivered', '2023-08-20'),
    (13, 9,  2,  1,  49.99, 'delivered', '2023-09-10'),
    (14,10,  7,  2,  39.98, 'cancelled', '2023-10-25'),
    (15,11, 15,  1, 129.99, 'pending',   '2024-02-01'),
    (16,12, 14,  1,  44.99, 'delivered', '2023-11-15'),
    (17,14,  3,  1, 119.99, 'delivered', '2023-12-20'),
    (18,15,  5,  2,  49.98, 'delivered', '2024-01-20'),
    (19,16, 11,  1,  79.99, 'delivered', '2023-07-10'),
    (20,17, 12,  1,  99.99, 'cancelled', '2023-08-05'),
    (21,18,  8,  5,  74.95, 'delivered', '2023-09-25'),
    (22,19,  9,  1,  59.99, 'delivered', '2023-10-10'),
    (23,20, 10,  1,  39.99, 'delivered', '2023-11-05'),
    (24,24,  4,  2,  69.98, 'delivered', '2023-12-15'),
    (25,25,  6,  1,  89.99, 'pending',   '2024-02-10'),
    (26, 1, 14,  1,  44.99, 'delivered', '2024-01-25'),
    (27, 2,  7,  3,  59.97, 'delivered', '2024-02-05'),
    (28, 4, 15,  1, 129.99, 'delivered', '2024-02-20'),
    (29, 6, 18,  4,  99.96, 'delivered', '2024-03-01'),
    (30, 8,  2,  2,  99.98, 'pending',   '2024-03-10'),
    (31,12, 19,  1,  39.99, 'delivered', '2024-03-15'),
    (32,17,  4,  1,  34.99, 'delivered', '2024-01-30'),
    (33,20,  1,  3,  89.97, 'cancelled', '2024-02-15'),
    (34,25, 11,  1,  79.99, 'delivered', '2024-03-20'),
    (35,15, 10,  1,  39.99, 'pending',   '2024-03-25'),
    (36, 9, 18,  2,  49.98, 'delivered', '2024-01-15'),
    (37,11,  8,  2,  29.98, 'delivered', '2024-02-25'),
    (38,16, 13,  1, 149.99, 'cancelled', '2024-03-05'),
    (39,18, 19,  2,  79.98, 'delivered', '2024-03-12'),
    (40, 3, 14,  1,  44.99, 'delivered', '2024-03-18'),
]

# Only for delivered orders. Products 16, 17, 20 never ordered.
RETURNS_DATA = [
    (1,   2, 'Changed mind',  'approved', '2023-05-25'),
    (2,   7, 'Damaged',       'approved', '2023-09-10'),
    (3,   8, 'Wrong item',    'pending',  '2023-10-25'),
    (4,   9, 'Quality issue', 'rejected', '2023-12-01'),
    (5,  12, 'Damaged',       'approved', '2023-09-05'),
    (6,  13, 'Changed mind',  'approved', '2023-09-25'),
    (7,  16, 'Wrong item',    'pending',  '2023-11-30'),
    (8,  21, 'Quality issue', 'approved', '2023-10-10'),
    (9,  22, 'Damaged',       'rejected', '2023-10-25'),
    (10, 24, 'Changed mind',  'pending',  '2024-01-05'),
    (11, 26, 'Wrong item',    'approved', '2024-02-10'),
    (12, 29, 'Damaged',       'approved', '2024-03-15'),
]

# order_id=None means general inquiry not related to any order
SERVICE_REQUESTS_DATA = [
    (1,   1,  2, 'Order not delivered',         'high',   'open',        '2023-05-20'),
    (2,   4,  7, 'Product damaged on arrival',  'high',   'closed',      '2023-09-05'),
    (3,   5,  9, 'Refund request',              'medium', 'closed',      '2023-11-25'),
    (4,   8,  None, 'Account access issue',     'medium', 'in_progress', '2024-01-10'),
    (5,  12, 16, 'Item description mismatch',   'low',    'closed',      '2023-12-01'),
    (6,   2,  None, 'Update billing address',   'low',    'closed',      '2024-01-15'),
    (7,   7, 11, 'Order status not updating',   'medium', 'open',        '2024-01-10'),
    (8,  15, 18, 'Wrong size delivered',        'high',   'in_progress', '2024-01-25'),
    (9,  17,  None, 'Cancel my account',        'medium', 'open',        '2024-02-01'),
    (10, 20, 23, 'Payment issue',               'high',   'closed',      '2023-11-10'),
    (11,  6, 29, 'Incorrect quantity received', 'medium', 'in_progress', '2024-03-05'),
    (12,  9,  None, 'Change delivery address',  'low',    'closed',      '2024-01-20'),
    (13, 25, 25, 'When will my order arrive?',  'low',    'open',        '2024-02-15'),
    (14, 11, 15, 'Product quality complaint',   'medium', 'in_progress', '2024-02-05'),
    (15,  3,  None, 'Newsletter unsubscribe',   'low',    'closed',      '2024-02-20'),
    (16, 14, 17, 'Warranty claim',              'high',   'open',        '2024-03-01'),
    (17, 19,  None, 'Account verification',     'medium', 'open',        '2024-03-10'),
    (18, 24, 33, 'Order cancellation request',  'high',   'closed',      '2024-02-20'),
]


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _create_schema(conn):
    conn.executescript("""
        PRAGMA foreign_keys = OFF;

        DROP TABLE IF EXISTS service_requests;
        DROP TABLE IF EXISTS returns;
        DROP TABLE IF EXISTS orders;
        DROP TABLE IF EXISTS products;
        DROP TABLE IF EXISTS users;

        CREATE TABLE users (
            id            INTEGER PRIMARY KEY,
            name          TEXT    NOT NULL,
            email         TEXT    NOT NULL,
            age           INTEGER,
            city          TEXT,
            phone         TEXT,
            registered_at TEXT,
            is_active     INTEGER DEFAULT 1
        );

        CREATE TABLE products (
            id         INTEGER PRIMARY KEY,
            name       TEXT NOT NULL,
            category   TEXT,
            price      REAL,
            stock      INTEGER,
            created_at TEXT
        );

        CREATE TABLE orders (
            id          INTEGER PRIMARY KEY,
            user_id     INTEGER REFERENCES users(id),
            product_id  INTEGER REFERENCES products(id),
            quantity    INTEGER,
            total_price REAL,
            status      TEXT,
            ordered_at  TEXT
        );

        CREATE TABLE returns (
            id          INTEGER PRIMARY KEY,
            order_id    INTEGER REFERENCES orders(id),
            reason      TEXT,
            status      TEXT,
            returned_at TEXT
        );

        CREATE TABLE service_requests (
            id         INTEGER PRIMARY KEY,
            user_id    INTEGER REFERENCES users(id),
            order_id   INTEGER REFERENCES orders(id),
            subject    TEXT,
            priority   TEXT,
            status     TEXT,
            created_at TEXT
        );

        PRAGMA foreign_keys = ON;
    """)


def _insert_data(conn):
    conn.executemany(
        "INSERT INTO users VALUES (?,?,?,?,?,?,?,?)", USERS_DATA
    )
    conn.executemany(
        "INSERT INTO products VALUES (?,?,?,?,?,?)", PRODUCTS_DATA
    )
    conn.executemany(
        "INSERT INTO orders VALUES (?,?,?,?,?,?,?)", ORDERS_DATA
    )
    conn.executemany(
        "INSERT INTO returns VALUES (?,?,?,?,?)", RETURNS_DATA
    )
    conn.executemany(
        "INSERT INTO service_requests VALUES (?,?,?,?,?,?,?)", SERVICE_REQUESTS_DATA
    )
    conn.commit()


def init_db():
    conn = get_connection()
    _create_schema(conn)
    _insert_data(conn)
    conn.close()


def reset_db():
    init_db()


def get_tables_data(table_count):
    tables = TABLE_ORDER[:table_count]
    conn = get_connection()
    result = {}
    for name in tables:
        cursor = conn.execute(f"SELECT * FROM {name}")
        columns = [desc[0] for desc in cursor.description]
        rows = [list(row) for row in cursor.fetchall()]
        result[name] = {'columns': columns, 'rows': rows}
    conn.close()
    return result
