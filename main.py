import hashlib
import sqlite3
from fastapi import FastAPI, Depends # Librería API
import uvicorn # Libreria de servidor local
from app.routers import user, payment, notification, group
from app.database.database import Base, engine

app = FastAPI()
app.include_router(user.router)
app.include_router(payment.router)
app.include_router(notification.router)
app.include_router(group.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
    
@app.get("/reload")
def reloadDb():
    con = sqlite3.connect("app/database/local.db")

    cur = con.cursor()

    sql_statements = [
    "DROP TABLE IF EXISTS user;",
    """
    CREATE TABLE user (
        email TEXT PRIMARY KEY,
        username TEXT UNIQUE,
        password TEXT NOT NULL,
        image TEXT DEFAULT 'https://i.discogs.com/_kK2FFfyrhNnbdTjCGMqfy_2gsMw120aUhKTb3M9kyE/rs:fit/g:sm/q:40/h:300/w:300/czM6Ly9kaXNjb2dz/LWRhdGFiYXNlLWlt/YWdlcy9SLTEzMTk5/NTg3LTE1NDk4MTEy/MjMtNTczMC5qcGVn.jpeg'
    );
    """,
    "DROP TABLE IF EXISTS groups;",
    """
    CREATE TABLE groups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        group_name TEXT NOT NULL,
        image TEXT DEFAULT 'https://static.vecteezy.com/system/resources/previews/023/547/344/non_2x/group-icon-free-vector.jpg'
    );
    """,
    "DROP TABLE IF EXISTS user_group;",
    """
    CREATE TABLE user_group (
        user_email TEXT,
        group_id INTEGER,
        is_admin BOOLEAN DEFAULT FALSE,
        PRIMARY KEY(user_email, group_id),
        FOREIGN KEY(user_email) REFERENCES user(email),
        FOREIGN KEY(group_id) REFERENCES groups(id)
    );
    """,
    "DROP TABLE IF EXISTS notification;",
    """
    CREATE TABLE notification (
        notif_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_email TEXT,
        group_id INTEGER,
        notif_date DATE,
        FOREIGN KEY(user_email) REFERENCES user(email),
        FOREIGN KEY(group_id) REFERENCES groups(id)
    );
    """,
    "DROP TABLE IF EXISTS payment;",
    """
    CREATE TABLE payment (
        payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        payer_email TEXT,
        group_id INTEGER,
        payment_date DATE,
        payment_args TEXT NOT NULL,
        total_payment REAL NOT NULL,
        FOREIGN KEY(payer_email) REFERENCES user(email),
        FOREIGN KEY(group_id) REFERENCES groups(id)
    );
    """,
    "DROP TABLE IF EXISTS user_payment;",
    """
    CREATE TABLE user_payment (
        payment_id INTEGER,
        user_email TEXT,
        quantity REAL DEFAULT 0,
        paid BOOLEAN DEFAULT FALSE,
        PRIMARY KEY(payment_id, user_email),
        FOREIGN KEY(payment_id) REFERENCES payment(payment_id),
        FOREIGN KEY(user_email) REFERENCES user(email)
    );
    """
    ]

    for sql in sql_statements:
        cur.execute(sql)

    cur.execute("INSERT INTO user (email, username, password) VALUES (?, ?, ?)", 
                ('erik@gmail.com', 'ErikAT', hashlib.sha256("erik".encode()).hexdigest()))

    cur.execute("INSERT INTO groups (group_name) VALUES (?)", 
                ('Grupo de prueba',))

    cur.execute("INSERT INTO user_group (user_email, group_id, is_admin) VALUES (?, ?, ?)", 
                ('erik@gmail.com', 1, 1))

    users = [
    ('prueba1@gmail.com', 'Prueba1', hashlib.sha256("prueba".encode()).hexdigest(), 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQyKcjZ-kU3-GrVs1pmdnb8zQf2mtXDB2R1Uw&s'),
    ('prueba2@gmail.com', 'Prueba2', hashlib.sha256("prueba".encode()).hexdigest(), 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQHBWVZVRa616uJT9aj_L_tJwVB3X8c9EZaIw&s'),
    ('prueba3@gmail.com', 'Prueba3', hashlib.sha256("prueba".encode()).hexdigest(), 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/User_icon_2.svg/800px-User _icon_2.svg.png'),
    ('prueba4@gmail.com', 'Prueba4', hashlib.sha256("prueba".encode()).hexdigest(), 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT8GDrMMZ3vCvSZHCYRrj9AvIOIN5rZIXDyKA&s'),
    ('prueba5@gmail.com', 'Prueba5', hashlib.sha256("prueba".encode()).hexdigest(), 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR_C0bk8a08vSD6T_mKMrLqhRIxjQwcSheZTQ&s')
    ]

    cur.executemany("INSERT INTO user (email, username, password, image) VALUES (?, ?, ?, ?)", users)

    user_groups = [
    ('prueba1@gmail.com', 1),
    ('prueba2@gmail.com', 1),
    ('prueba3@gmail.com', 1),
    ('prueba4@gmail.com', 1)
    ]

    cur.executemany("INSERT INTO user_group (user_email, group_id) VALUES (?, ?)", user_groups)

    cur.execute("INSERT INTO payment (payer_email, group_id , payment_date, payment_args, total_payment) VALUES (?, ?, '2025-02-04', ?, ?)", 
                ('prueba1@gmail.com', 1, 'Concepto de Prueba', 45))

    user_payments = [
    (1, 'prueba2@gmail.com', 15, 0),
    (1, 'prueba3@gmail.com', 15, 0),
    (1, 'prueba4@gmail.com', 15, 1)
    ]

    cur.executemany("INSERT INTO user_payment (payment_id, user_email, quantity, paid) VALUES (?, ?, ?, ?)", user_payments)

    cur.execute("INSERT INTO notification (user_email, group_id, notif_date) VALUES (?, ?, CURRENT_TIMESTAMP)", 
                ('prueba5@gmail.com', 1))

    con.commit()

    con.close()

