from src.api import SuperJobAPI, HeadHunterAPI


def get_user_input(DB):
    """
    Запрашивает у пользователя информацию о платформе, поисковом запросе,
    фильтре по зарплате и количестве вакансий для отображения.
    Возвращает введенные значения.
    """
    platform = 'HH'
    search_query = input("Введите поисковый запрос для поиска HH: ")
    salary_filter = input("Введите минимальную зарплату для фильтра (или оставьте пустым): ")
    vacancies_count = int(input("Введите количество вакансий для отображения: "))
    search_vacancies(platform, search_query, salary_filter, vacancies_count, DB)


def search_vacancies(platform, search_query, salary_filter, vacancies_count, DB):
    """
    Основная функция, выполняющая поиск вакансий на выбранной платформе
    и сохранение результатов в файл vacancies.json.
    """
    if platform == 'BOTH':
        platforms = ['SJ', 'HH']
    else:
        platforms = [platform]

    for i in platforms:
        api = SuperJobAPI() if i == 'SJ' else HeadHunterAPI()

        for vacancy in api.get_vacancies_with_filters(keywords=search_query, salary=salary_filter,
                                                      word_count=vacancies_count):
            employer_id = api.get_employer_by_vacancy_id(vacancy.vacancy_id)
            DB.add_employer(api.get_employer_info(employer_id))
            DB.add_vacancy(vacancy, api.get_employer_by_vacancy_id(vacancy.vacancy_id))
            print(vacancy)
            print('=' * 120)


def company_search(DB):
    """
    Выполняет поиск компании на HeadHunter по названию и выводит информацию о ней,
    а также список вакансий компании.

    :param DB: Объект базы данных, используемый для сохранения результатов.
    :type DB: Database
    """
    employer_name = input('Введите название компании, которую хотите найти на HH.ru: ')
    hh = HeadHunterAPI()
    req = hh.get_employers_list(employer_name)
    for employer in req:
        DB.add_employer(employer)
        print('=' * 25)
        print(employer)
    employer_id = input('=' * 25 + '\nВведите id компании, которая вам подходит: ')
    for vacancy in hh.get_all_employers_vacancy(employer_id):
        DB.add_vacancy(vacancy, employer_id)
        print(vacancy)


def search_by_id(DB):
    """
    Выполняет поиск вакансии на HeadHunter по id и выводит информацию о ней.

    :param DB: Объект базы данных, используемый для сохранения результатов.
    :type DB: Database
    """
    api = HeadHunterAPI()
    get_id = input('Введите id вакансии:\n')

    vacancy = api.get_vacancy_by_id(get_id)
    employer_id = api.get_employer_by_vacancy_id(vacancy.vacancy_id)
    DB.add_employer(api.get_employer_info(employer_id))
    DB.add_vacancy(vacancy, api.get_employer_by_vacancy_id(vacancy.vacancy_id))
    print('=' * 25)
    print(vacancy)
    print('=' * 25)


def search_by_keyword(DB):
    """
    Выполняет поиск вакансий на HeadHunter по ключевому слову и выводит информацию о них.

    :param DB: Объект базы данных, используемый для сохранения результатов.
    :type DB: Database
    """
    api = HeadHunterAPI()
    keyword = input('Введите ключевое слово:\n')

    for vacancy in api.get_vacancies_by_keywords(keyword, 100):
        employer_id = api.get_employer_by_vacancy_id(vacancy.vacancy_id)
        DB.add_employer(api.get_employer_info(employer_id))
        DB.add_vacancy(vacancy, api.get_employer_by_vacancy_id(vacancy.vacancy_id))
        print('=' * 25)
        print(vacancy)
        print('=' * 25)