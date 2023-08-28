from dbm_manager.db_manager import DBManager
from api_handler.hh_handler import getEmployers, insertEmployers, get_vacancies, insertVacancy
from dbm_manager.table_сreate import TableCreator
import psycopg2
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

params = config['postgresql']

conn = psycopg2.connect(
    host=params['host'],
    database=params['database'],
    user=params['user'],
    password=params['password']
)

keyword = "Менеджер"  # Ключевое слово для запроса №5
employer_ids = [64174, 6, 3529, 80, 1740, 3127, 2180, 196621, 3776, 7944]  # Заготовленный список ID компаний


def print_menu():
    print('-----------------------------------------------------------------------------------------------------------')
    print('| 1 - Вывести список всех компаний и количество вакансий                                                  |')
    print('| 2 - Вывести список всех вакансий с указанием компании, названия вакансии, зарплаты и ссылки на вакансию |')
    print('| 3 - Вывести среднюю зарплату по вакансиям.                                                              |')
    print('| 4 - Вывести список всех вакансий, у которых зарплата выше средней по всем вакансиям                     |')
    print('| 5 - Вывести список всех вакансий, по ключевому слову, например python.                                  |')
    print('| 6 - выход                                                                                               |')
    print('-----------------------------------------------------------------------------------------------------------')


def main():
    table_creator = TableCreator(
        host=params['host'],
        database=params['database'],
        user=params['user'],
        password=params['password']
    )

    table_creator.drop_tables()     # Удаляем таблицы
    table_creator.create_employers_table()      # Создаем таблицу employers
    table_creator.create_vacancies_table()      # Создаем таблицу vacancies

    employers = getEmployers(employer_ids)      # Получаем работодателей

    """ Заполняем таблицу employers """
    insertEmployers(
        employers,
        host=params['host'],
        database=params['database'],
        user=params['user'],
        password=params['password']
    )
    vacancies = get_vacancies(employer_ids)     # Получаем вакансии

    """ Заполняем таблицу vacancies """
    insertVacancy(
        vacancies,
        host=params['host'],
        database=params['database'],
        user=params['user'],
        password=params['password']
    )

    """ Создаем экземпляр класса  DBManager"""
    db_manager = DBManager(
        host=params['host'],
        database=params['database'],
        user=params['user'],
        password=params['password']
    )

    vacancies_1 = db_manager.get_companies_and_vacancies_count()
    vacancies_2 = db_manager.get_all_vacancies()
    vacancies_3 = db_manager.get_avg_salary()
    vacancies_4 = db_manager.get_vacancies_with_higher_salary()
    vacancies_5 = db_manager.get_vacancies_with_keyword(keyword)

    while True:
        print_menu()
        choice = input('Выберите действие: ')
        if choice == '1':
            for vac_1 in vacancies_1:
                print(f"Организация: {vac_1[0]}, кол. вакансий: {vac_1[1]}")
                print()
        elif choice == '2':
            for vac_2 in vacancies_2:
                name = vac_2[0]
                vacancy_name = vac_2[1]
                salary = vac_2[2]
                url = vac_2[3]
                print(f"Организация: {name}, вакансия: {vacancy_name}, зарплата: {salary}, ссылка: {url}")
        elif choice == '3':
            print(f'Name: Средняя зарплата: {int(vacancies_3)}')
        elif choice == '4':
            for vac_4 in vacancies_4:
                name = vac_4[0]
                vacancy_name = vac_4[1]
                salary = vac_4[2]
                url = vac_4[3]
                print(f"Организация: {name}, вакансия: {vacancy_name}, зарплата: {salary}, ссылка: {url}")
        elif choice == '5':
            for vac_5 in vacancies_5:
                name = vac_5[0]
                vacancy_name = vac_5[1]
                salary = vac_5[2]
                url = vac_5[3]
                print(f"Организация: {name}, вакансия: {vacancy_name}, вакансия: {salary}, ссылка: {url}")
        elif choice == '6':
            break
        else:
            print('Неверный выбор. Попробуйте еще раз.')
            print()


if __name__ == '__main__':
    main()