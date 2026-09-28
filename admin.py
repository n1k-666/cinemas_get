import psycopg2
from config import host, user, password, db_name, port

try:
    def f():
        # создание таблицы городов
        with connection.cursor() as cursor:
            cursor.execute(
                '''CREATE TABLE cities(
                    id serial PRIMARY KEY,
                    name VARCHAR(100) NOT NULL UNIQUE);'''
            )

            print("[INFO] table cities created")

        # создание таблицы кинотеатров

        with connection.cursor() as cursor:
            cursor.execute(
                '''CREATE TABLE cinemas(
                    id serial PRIMARY KEY,
                    city_id INTEGER NOT NULL REFERENCES cities(id) ON DELETE CASCADE,
                    address VARCHAR(255) NOT NULL);'''
            )

            print("[INFO] table cinemas created")

        # ввод данных городов
        with connection.cursor() as cursor:
            cursor.execute(
                '''INSERT INTO cities (name) VALUES
                ('Москва'),
                ('Санкт-Петербург'),
                ('Казань'),
                ('Новосибирск'),
                ('Екатеринбург');'''
            )

            print("[INFO] cities data created")

        # ввод данных кинотеатров

        with connection.cursor() as cursor:
            cursor.execute(
                '''INSERT INTO cinemas (city_id, address) VALUES
                ((SELECT id FROM cities WHERE name='Москва'), 'ул. Арбат, 1'),
                ((SELECT id FROM cities WHERE name='Москва'), 'пр. Мира, 10'),
                ((SELECT id FROM cities WHERE name='Москва'), 'ул. Тверская, 5'),
                ((SELECT id FROM cities WHERE name='Москва'), 'Ленинградский пр., 20'),
                ((SELECT id FROM cities WHERE name='Москва'), 'ул. Новый Арбат, 15'),
                ((SELECT id FROM cities WHERE name='Москва'), 'Кутузовский пр., 30'),
                ((SELECT id FROM cities WHERE name='Москва'), 'ул. Пятницкая, 8'),
                ((SELECT id FROM cities WHERE name='Санкт-Петербург'), 'Невский пр., 1'),
                ((SELECT id FROM cities WHERE name='Санкт-Петербург'), 'Лиговский пр., 10'),
                ((SELECT id FROM cities WHERE name='Санкт-Петербург'), 'ул. Рубинштейна, 5'),
                ((SELECT id FROM cities WHERE name='Санкт-Петербург'), 'Московский пр., 20'),
                ((SELECT id FROM cities WHERE name='Санкт-Петербург'), 'Садовая ул., 7'),
                ((SELECT id FROM cities WHERE name='Санкт-Петербург'), 'наб. Фонтанки, 12'),
                ((SELECT id FROM cities WHERE name='Казань'), 'ул. Баумана, 1'),
                ((SELECT id FROM cities WHERE name='Казань'), 'пр. Победы, 2'),
                ((SELECT id FROM cities WHERE name='Казань'), 'ул. Пушкина, 3'),
                ((SELECT id FROM cities WHERE name='Казань'), 'ул. Кремлёвская, 4'),
                ((SELECT id FROM cities WHERE name='Казань'), 'ул. Достоевского, 5'),
                ((SELECT id FROM cities WHERE name='Новосибирск'), 'Красный пр., 1'),
                ((SELECT id FROM cities WHERE name='Новосибирск'), 'ул. Ленина, 2'),
                ((SELECT id FROM cities WHERE name='Новосибирск'), 'ул. Кирова, 3'),
                ((SELECT id FROM cities WHERE name='Екатеринбург'), 'пр. Ленина, 1');
                '''
            )

            print("[INFO] cinemas data created")

    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        dbname=db_name,
        port=port
    )
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT version();'
        )

        print(f'server version: {cursor.fetchone()}')

    #заполнение таблицы
    #f()


    # извлечение данных
    with connection.cursor() as cursor:
        cursor.execute(
            '''SELECT c.name AS city, COUNT(cin.id) AS cinemas_count
            FROM cities c
            JOIN cinemas cin ON cin.city_id = c.id
            GROUP BY c.id, c.name
            HAVING COUNT(cin.id) > 5
            ORDER BY cinemas_count DESC;'''
        )
        rows = cursor.fetchall()
        for row in rows:
            print(row)



except Exception as _ex:
    print('[INFO] error: ', _ex)
finally:
    if connection:
        connection.close()
        print('[INFO] Connect closs')