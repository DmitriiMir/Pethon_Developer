import sqlite3


def get_db_connection():
    conn = sqlite3.connect(
        'database_module_14_5.db')
    return conn


def initiate_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS Products')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            price INTEGER NOT NULL,
            image_url TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER NOT NULL,
            balance INTEGER NOT NULL DEFAULT 1000
        )
    ''')

    conn.commit()
    conn.close()
    print("Таблицы Products и Users пересозданы или уже существуют.")


def get_all_products():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()

    conn.close()
    return products


def insert_dummy_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM Products")
    count = cursor.fetchone()[0]

    if count == 0:
        products = [
            {"title": "Мультивитамины для женщин UltraBalance",
             "description": "Комплекс витаминов и минералов для взрослых 60 таблеток",
             "price": 1454,
             "image_url": "https://ir-2.ozone.ru/s3/multimedia-2/wc1000/6607026362.jpg"},

            {"title": "Инозитол 1000 мг капсулы UltraBalance",
             "description": "БАД комплекс для женского здоровья миоинозитол витамин для женщин и мужчин",
             "price": 1523,
             "image_url": "https://ir-2.ozone.ru/s3/multimedia-e/wc1000/6764941634.jpg"},

            {"title": "Витамины для женщин и мужчин",
             "description": "Общий комплекс 13+10, 90 капсул",
             "price": 566,
             "image_url": "https://ir-2.ozone.ru/s3/multimedia-1-n/wc1000/7076872103.jpg"},

            {"title": "Цинк хелат",
             "description": "Цинк хелат 25 мг, 90 таблеток / NFO Норвегия",
             "price": 1905,
             "image_url": "https://ir-2.ozone.ru/s3/multimedia-3/wc1000/6825233847.jpg"}
        ]

        for product in products:
            cursor.execute("INSERT INTO Products (title, description, price, image_url) VALUES (?, ?, ?, ?)",
                           (product['title'], product['description'], product['price'], product['image_url']))

        conn.commit()
        print("Новые данные для Products добавлены.")
    else:
        print("Таблица Products уже содержит данные, вставка пропущена.")

    conn.close()


def add_user(username, email, age):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO Users (username, email, age) VALUES (?, ?, ?)", (username, email, age))
    conn.commit()
    conn.close()


def is_included(username):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM Users WHERE username = ?", (username,))
    count = cursor.fetchone()[0]

    conn.close()
    return count > 0


if __name__ == "__main__":
    initiate_db()
    insert_dummy_data()

    products = get_all_products()
    for product in products:
        print(
            f"ID: {product[0]}, Название: {product[1]}, Описание: {product[2]}, Цена: {product[3]}, URL изображения: {product[4]}")