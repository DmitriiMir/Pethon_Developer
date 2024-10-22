import sqlite3

def get_db_connection():
    conn = sqlite3.connect('database.db')
    return conn

def initiate_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            price INTEGER NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
    print("Таблица Products создана или уже существует.")


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
        cursor.execute("INSERT INTO Products (title, description, price) VALUES ('Мультивитамины для женщин UltraBalance', 'Комплекс витаминов и минералов для взрослых 60 таблеток', 1454)")
        cursor.execute("INSERT INTO Products (title, description, price) VALUES ('Инозитол 1000 мг капсулы UltraBalance', 'БАД комплекс для женского здоровья миоинозитол витамин для женщин и мужчин', 1523)")
        cursor.execute("INSERT INTO Products (title, description, price) VALUES ('Витамины для женщин и мужчин', 'Общий комплекс 13+10, 90 капсул', 566)")
        cursor.execute("INSERT INTO Products (title, description, price) VALUES ('Цинк хелат', 'Цинк хелат 25 мг, 90 таблеток / NFO Норвегия', 1905)")
        conn.commit()
        print("Тестовые данные добавлены.")
    else:
        print("Таблица уже содержит данные, вставка пропущена.")

    conn.close()


if __name__ == "__main__":
    initiate_db()
    insert_dummy_data()

    products = get_all_products()
    for product in products:
        print(f"ID: {product[0]}, Название: {product[1]}, Описание: {product[2]}, Цена: {product[3]}")



