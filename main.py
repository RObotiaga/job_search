from src.api import SuperJobAPI, HeadHunterAPI
from src.WorkWithJSON import JSONVacancyFileManager


def get_user_input():
    """
    Запрашивает у пользователя информацию о платформе, поисковом запросе,
    фильтре по зарплате и количестве вакансий для отображения.
    Возвращает введенные значения.
    """
    platforms = ['SJ', 'HH', 'BOTH', 'FIF', ]
    platform = input(
       "Введите платформу: \nSJ - SuperJob\nHH - HeadHunter\nBOTH - Обе платформы\nFIF - поиск только в файле ").upper()
    while platform not in platforms:
        print("Неправильно выбрана платформа. Пожалуйста, выберите из следующих вариантов: SJ, HH, BOTH")
        platform = input("Введите платформу (SJ - SuperJob, HH - HeadHunter, BOTH - Обе платформы): ")
    search_query = input("Введите поисковый запрос: ")
    salary_filter = input("Введите минимальную зарплату для фильтра (или оставьте пустым): ")
    vacancies_count = int(input("Введите количество вакансий для отображения для каждого из сервисов: "))
    if platform == 'SJ' or platform == 'HH' or platform == 'BOTH':
        search_vacancies(platform, search_query, salary_filter, vacancies_count)
    elif platform == 'FIF':
        search_in_file(search_query, salary_filter, vacancies_count)


def search_vacancies(platform, search_query, salary_filter, vacancies_count):
    """
    Основная функция, выполняющая поиск вакансий на выбранной платформе
    и сохранение результатов в файл vacancies.json.
    """
    vacancies_file = "vacancies.json"

    if platform == 'BOTH':
        platforms = ['SJ', 'HH']
    else:
        platforms = [platform]

    file_manager = JSONVacancyFileManager(vacancies_file)

    for i in platforms:
        api = SuperJobAPI() if i == 'SJ' else HeadHunterAPI()

        for vacancy in api.get_vacancies_with_filters(keywords=search_query, salary=salary_filter,
                                                      word_count=vacancies_count):
            file_manager.add_vacancy(vacancy)
            print(vacancy)
            print()
            print('=' * 120)
            print()
    search_from_file = input("Хотите ли вы искать вакансии в файле? (Y/N): ")
    if search_from_file.upper() == 'Y':
        search_in_file(search_query, salary_filter, vacancies_count)


def search_in_file(search_query, salary_filter, vacancies_count):
    """
    Функция для поиска вакансии в файле и его редактирования
    и сохранение результатов в файл vacancies.json.
    """
    vacancies_file = "vacancies.json"
    file_manager = JSONVacancyFileManager(vacancies_file)

    keywords = [search_query]

    if salary_filter:
        vacancies_from_file = file_manager.get_vacancies_by_salary_and_keywords(int(salary_filter), keywords)
    else:
        vacancies_from_file = file_manager.get_vacancies_by_keywords(keywords)

    if vacancies_from_file:
        vacancies_from_file = vacancies_from_file[:vacancies_count]
        for vacancy in vacancies_from_file:
            print(vacancy)
            print()
            print('=' * 120)
            print()
    else:
        print("По вашему запросу в файле вакансий не найдено.")
    del_vacancy = input('Если вы хотите удалить вакансию из файла введите ее ID(можно несколько)\nВыйти - q')
    if int(del_vacancy):
        for vacancy in del_vacancy.split(' '):
            file_manager.delete_vacancy(vacancy)
    else:
        return


while True:
    get_user_input()
