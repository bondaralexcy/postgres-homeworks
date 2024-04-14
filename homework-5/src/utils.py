import json
import psycopg2

def create_database(params, db_name) -> None:
    """Создает новую базу данных."""
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
    cur.execute(f"CREATE DATABASE {db_name}")

    conn.close()


def execute_sql_script(cur, script_file) -> None:
    """Выполняет скрипт из файла для заполнения БД данными."""

    fd = open(script_file, 'r')
    sql_file = fd.read()
    cur.execute(sql_file)
    cur.execute(
        """
        ALTER TABLE products ADD COLUMN supplier_id integer
        """
    )
    fd.close()


def create_suppliers_table(cur) -> None:
    """Создает таблицу suppliers."""

    cur.execute("""CREATE TABLE suppliers (
        supplier_id SERIAL PRIMARY KEY,
        company_name varchar(40) NOT NULL,
        contact_name varchar(50),
        address varchar(100),
        phone varchar(24),
        fax varchar(24)
        )
    """)


def get_suppliers_data(json_file: str) -> list[dict]:
    """Извлекает данные о поставщиках из JSON-файла и возвращает список словарей с соответствующей информацией."""
    with open('suppliers.json', 'r', encoding='utf8') as file:
        data = json.load(file)
    return data


def insert_suppliers_data(cur, suppliers: list[dict]) -> None:
    """Добавляет данные из suppliers.json в таблицу suppliers."""
    for data_suppliers in suppliers:
        cur.execute(
            """
            INSERT INTO suppliers (company_name, contact_name, address, phone, fax)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING supplier_id
            """,
            (data_suppliers['company_name'], data_suppliers['contact'], data_suppliers['address'], data_suppliers['phone'], data_suppliers['fax'])
        )

        supplier_id = cur.fetchone()[0]

        for product_one in data_suppliers['products']:
            cur.execute(
                """ SELECT product_id FROM products WHERE product_name = %(poduct)s""", {'poduct': product_one}
            )

            product_id = cur.fetchone()[0]

            cur.execute(
                """UPDATE products SET supplier_id = %(suppl)s WHERE product_id= %(prod)s""",
                {'suppl': supplier_id, 'prod': product_id}
            )


def add_foreign_keys(cur, json_file) -> None:
    """Добавляет foreign key со ссылкой на supplier_id в таблицу products."""
    cur.execute(
        """ALTER TABLE ONLY products
    ADD CONSTRAINT fk_products_suppliers FOREIGN KEY (supplier_id) REFERENCES suppliers; """
    )
