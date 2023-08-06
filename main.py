from src.DBManager import DBManager
from site_search import get_user_input, company_search, search_by_id, search_by_keyword


def hello():
    DB = DBManager("JobSearch", "postgres", "localhost")
    choose_mode = input('Выберите режим:\nБД - Работа с БД    ХХ - Работа с HeadHunter\n')
    if choose_mode.upper() == 'ХХ':
        search_vacancy_hh(DB)
    elif choose_mode.upper() == 'БД':
        search_in_db(DB)
    else:
        print('Нет такого режима')
        hello()


def search_in_db(DB):
    for vacancy in DB.get_all_vacancies():
        print(f'Компания: {vacancy[0]}\n{vacancy[1]}\nЗ/П: {vacancy[2]}\nURL: {vacancy[3]}\n' + '=' * 25)
    while True:
        choose_command = int(
            input(
                '\nВыберите действие: \n1) Удалить вакансию\n2) Найти вакансию по ключевому слову\n3) Получить список '
                'всех компаний и количество вакансий у компании\n4) Узнать среднюю зарплату по вакансии\n5) Получить '
                'список вакансий с зарплатой выше средней\n\n6) Закончить\n'))
        if choose_command == 1:
            vacancy_n = input('Введите номер вакансии:')
            DB.delete_vacancy(vacancy_n)
        elif choose_command == 2:
            keyword = input('Введите ключевое слово:')
            for vacancy in DB.get_vacancies_with_keyword(keyword):
                print(f'Компания: {vacancy[0]}\n{vacancy[1]}\nЗ/П: {vacancy[2]}\nURL: {vacancy[3]}\n' + '=' * 25)
        elif choose_command == 3:
            for vacancy in DB.get_all_vacancies():
                print(f'Компания:{vacancy[0]}\n{vacancy[1]}\nЗ/П:{vacancy[2]}\nURL: {vacancy[3]}')
        elif choose_command == 4:
            print(f'Средняя З/П {int(DB.get_avg_salary())}')
        elif choose_command == 5:
            for vacancy in DB.get_vacancies_with_higher_salary():
                print(f'Компания:{vacancy[0]}\n{vacancy[1]}\nЗ/П: {vacancy[2]}\nURL: {vacancy[3]}')
        elif choose_command == 6:
            break


def search_vacancy_hh(DB):
    choose_mode = int(input(
        'Выберите режим поиска:\n1) Поиск по компаниям\n2) Поиск id вакансии\n3) Поиск по ключевому слову\n4) '
        'Расширенный поиск\n'))

    if choose_mode == 1:
        company_search(DB)
    elif choose_mode == 2:
        search_by_id(DB)
    elif choose_mode == 3:
        search_by_keyword(DB)
    elif choose_mode == 4:
        get_user_input(DB)


hello()
