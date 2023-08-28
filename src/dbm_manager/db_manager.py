import psycopg2


class DBManager:
    """
    Класс для управления базой данных в PostgreSQL.
    """
    def __init__(self, host, database, user, password):
        self.conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )

    def get_companies_and_vacancies_count(self):
        """
        Возвращает список содержащий имя каждого работодателя и количество имеющихся у него вакансий.
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT employers.name, COUNT(*) AS vacancies_count
                FROM vacancies
                JOIN employers ON vacancies.employer_id = employers.employer_id
                GROUP BY employers.name
            """)
            return cur.fetchall()

    def get_all_vacancies(self):
        """
        Возвращает список содержащих имя работодателя, название вакансии, зарплату и URL-адрес каждой вакансии.
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT employers.name, vacancy_name, salary, url
                FROM vacancies
                JOIN employers ON vacancies.employer_id = employers.employer_id
            """)
            return cur.fetchall()

    def get_avg_salary(self):
        """
        Возвращает среднюю зарплату для всех вакансий в базе данных.
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT AVG(salary) AS avg_salary
                FROM vacancies
            """)
            return cur.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        """
        Возвращает список содержащий имя работодателя, название вакансии, зарплату и URL-адрес каждой вакансии
        с зарплатой выше средней.
        """
        avg_salary = self.get_avg_salary()
        with self.conn.cursor() as cur:
            cur.execute(f"""
                SELECT employers.name, vacancy_name, salary, url
                FROM vacancies
                JOIN employers ON vacancies.employer_id = employers.employer_id
                WHERE salary > {avg_salary}
            """)
            return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        """
        Возвращает список содержащий имя работодателя, название вакансии, зарплату и URL-адрес каждой вакансии,
        в названии которой содержится заданное ключевое слово.
        """
        with self.conn.cursor() as cur:
            cur.execute(f"""
                SELECT employers.name, vacancy_name, salary, url
                FROM vacancies
                JOIN employers ON vacancies.employer_id = employers.employer_id
                WHERE vacancy_name LIKE '%{keyword}%'
            """)
            return cur.fetchall()
