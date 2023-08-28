import psycopg2


class TableCreator:
    """
    Класс для создания и удаления таблиц в базе данных PostgreSQL.
    """
    def __init__(self, host, database, user, password):
        self.conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )

    def create_employers_table(self):
        """
        Создает таблицу «работодатели» в базе данных PostgreSQL.
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE employers (
                    employer_id INTEGER PRIMARY KEY,
                    name varchar(100)
                )
            """)
        self.conn.commit()

    def create_vacancies_table(self):
        """
        Создает таблицу «вакансии» в базе данных PostgreSQL.
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE vacancies (
                    employer_id INTEGER,
                    vacancy_name varchar(100),
                    salary int,
                    url TEXT,
                    FOREIGN KEY (employer_id) REFERENCES employers(employer_id)
                )
            """)
        self.conn.commit()

    def drop_tables(self):
        """
        Удаляет таблицы «работодатели» и «вакансии» из базы данных PostgreSQL.
        """
        with self.conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS vacancies")
            cur.execute("DROP TABLE IF EXISTS employers")
        self.conn.commit()