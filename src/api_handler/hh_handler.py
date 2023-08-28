import requests
import psycopg2

def getEmployers(employer_ids):
    """
    Учитывая список идентификаторов работодателей, извлекает имя каждого работодателя из API HeadHunter
    и возвращает словарь.
    """
    employers = {}

    for employer_id in employer_ids:
        response = requests.get(f'https://api.hh.ru/employers/{employer_id}')
        if response.status_code == 200:
            json_data = response.json()
            employers[employer_id] = json_data['name']

    return employers

def insertEmployers(employers, host, database, user, password):
    """
    Учитывая словарь идентификаторов и имен работодателей, заполняет базу данных PostgreSQL.
    """
    insert_query = "INSERT INTO employers (employer_id, name) VALUES (%s, %s);"
    with psycopg2.connect(host=host, database=database, user=user, password=password) as conn:
        with conn.cursor() as cur:
            for employer_id, name in employers.items():
                cur.execute(insert_query, (employer_id, name))
            conn.commit()

def get_vacancies(employer_ids):
    """
    Учитывая список идентификаторов работодателей, извлекает нужное количество вакансий для каждого работодателя и
    возвращает список всех вакансий.
    """
    vacancies = []

    for employer_id in employer_ids:
        params = {
            'employer_id': employer_id,
            'per_page': 10
        }
        req = requests.get('https://api.hh.ru/vacancies', params)
        data = req.json()
        req.close()

        for vacancy in data['items']:
            vacancies.append(vacancy)

    return vacancies

def get_salary_from_hh_vacancy(salary_dict):
    """
        Получает зарплату из словаря вакансий

        Возвращает:
        Возвращает 0, если словарь равен None
    """
    if salary_dict is not None:

        if salary_dict['from'] is not None:
            return salary_dict['from']
        else:
            return salary_dict['to']

    return 0

def insertVacancy(vacancies, host, database, user, password):
    """
    Вставляет данные вакансий в базу данных PostgreSQL.
    """
    conn = psycopg2.connect(host=host, database=database, user=user, password=password)
    cur = conn.cursor()

    # Extract data from the vacancy object
    for vacancy in vacancies:
        employer_id = vacancy['employer']['id']
        vacancy_name = vacancy['name']
        salary = get_salary_from_hh_vacancy(vacancy['salary'])
        url = vacancy['alternate_url']

    # Insert the data into the database
        cur.execute("INSERT INTO vacancies (employer_id, vacancy_name, salary, url) VALUES (%s, %s, %s, %s)",
                    (employer_id, vacancy_name, salary, url))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
