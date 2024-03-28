"""Скрипт для заполнения данными таблиц в БД Postgres."""
import csv
import psycopg2


def import_from_csv(fn: str):
    """ Импортирует данные из csv-файла 'fn' в список кортежей data_list"""
    csv_file = open(fn, 'r', encoding='utf-8')
    data_list = []
    line_number = 0
    try:
        data = csv.reader(csv_file)
        for row in data:
            row_tuple = tuple(row)
            if line_number > 0:
                data_list.append(row_tuple)
            line_number += 1
    finally:
        csv_file.close()
        return data_list


def fill_postgres_tables():
    """ Заполняет таблицы в базе данных north данными из соответствующих csv-файлов"""

    # Подключаемся к базе данных "north"
    conn = psycopg2.connect(host="localhost", database="north", user="postgres", password="135790")

    try:
        with conn:
            # Создаем объект cursor()
            with conn.cursor() as cur:
                employees_list = import_from_csv('north_data/employees_data.csv')
                cur.executemany("INSERT INTO employees VALUES (%s, %s, %s, %s, %s, %s)", employees_list)

                customer_list = import_from_csv('north_data/customers_data.csv')
                cur.executemany("INSERT INTO customers VALUES (%s, %s, %s)", customer_list)

                orders_list = import_from_csv('north_data/orders_data.csv')
                cur.executemany("INSERT INTO orders VALUES (%s, %s, %s, %s, %s)", orders_list)

    finally:
        conn.close()



if __name__ == '__main__':
    fill_postgres_tables()
