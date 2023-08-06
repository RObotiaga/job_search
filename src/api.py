import requests
import os
from src.vacancy import Vacancy
from abc import ABC, abstractmethod
from src.employer import Employer

SUPERJOB_API_KEY = os.environ.get('SUPERJOB_API_KEY')
headers = {'X-Api-App-Id': SUPERJOB_API_KEY}


class API(ABC):
    @abstractmethod
    def __init__(self):
        """
        Конструктор класса.
        """
        pass

    @staticmethod
    @abstractmethod
    def call_api(url_params=None):
        """
        Вызывает API и возвращает результат в виде списка объектов вакансий.
        """
        pass

    @staticmethod
    @abstractmethod
    def get_vacancy_by_id(vacancy_id):
        """
        Получает вакансию по ее идентификатору с помощью API и возвращает объект вакансии.
        """
        pass

    @abstractmethod
    def get_vacancies_by_salary(self, salary, word_count):
        """
        Получает вакансии с заданной зарплатой с помощью API и возвращает список объектов вакансий.
        """
        pass

    @abstractmethod
    def get_vacancies_by_keywords(self, keywords, word_count):
        """
        Получает вакансии по ключевым словам с помощью API и возвращает список объектов вакансий.
        """
        pass

    @abstractmethod
    def get_vacancies_with_filters(self, keywords=None, salary=None, word_count=None):
        """
        Получает вакансии с применением фильтров (ключевые слова, зарплата) с помощью API,
        возвращает список объектов вакансий.
        """
        pass


class SuperJobAPI(API):
    def __init__(self):
        pass

    @staticmethod
    def call_api(url_params=None):
        response = requests.get('https://api.superjob.ru/2.0/vacancies/', params=url_params, headers=headers)
        return response.json().get('objects', [])

    @staticmethod
    def get_vacancy_by_id(vacancy_id):
        response = requests.get(f'https://api.superjob.ru/2.0/vacancies/{vacancy_id}', params={},
                                headers=headers).json()
        return Vacancy(vacancy_id, response['link'], response['profession'], response['payment_from'],
                       response['candidat'], 'SJ')

    def get_vacancies_by_salary(self, salary, word_count):
        response = requests.get('https://api.superjob.ru/2.0/vacancies/',
                                params={'no_agreement': 1, 'payment_from': salary, 'count': word_count},
                                headers=headers).json()
        return [self.get_vacancy_by_id(i['id']) for i in response['objects']]

    def get_vacancies_by_keywords(self, keywords, word_count):
        vacancies_list = []
        for keyword in keywords:
            vacancies = requests.get('https://api.superjob.ru/2.0/vacancies/',
                                     params={'no_agreement': 1, 'keyword': keyword, 'count': word_count},
                                     headers=headers).json()
            vacancies_list.extend([self.get_vacancy_by_id(i['id']) for i in vacancies['objects']])
        return vacancies_list

    def get_vacancies_with_filters(self, keywords=None, salary=None, word_count=None):
        vacancies_list = []
        vacancies = requests.get('https://api.superjob.ru/2.0/vacancies/',
                                 params={'no_agreement': 1, 'payment_from': salary,
                                         'keywords': [[], [], keywords.split(' ')],
                                         'count': word_count}, headers=headers).json()
        vacancies_list.extend([self.get_vacancy_by_id(i['id']) for i in vacancies['objects']])
        return vacancies_list


class HeadHunterAPI(API):
    def __init__(self):
        super().__init__()

    @staticmethod
    def call_api(url_params=None):
        response = requests.get('https://api.hh.ru/vacancies', params=url_params).json()
        return response['items']

    @staticmethod
    def get_vacancy_by_id(vacancy_id):
        response = requests.get(f'https://api.hh.ru/vacancies/{vacancy_id}').json()
        return Vacancy(vacancy_id, f'https://api.hh.ru/vacancies/{vacancy_id}', response['name'],
                       response['salary']['from'],
                       response['description'], 'HH')

    def get_vacancies_by_salary(self, salary, word_count):
        response = requests.get(f'https://api.hh.ru/vacancies/',
                                params={'area': 113, 'salary_from': salary, 'only_with_salary': True,
                                        'per_page': word_count}).json()
        return [self.get_vacancy_by_id(i['id']) for i in response['items']]

    def get_vacancies_by_keywords(self, keywords, word_count):
        vacancies_list = []
        for keyword in keywords:
            vacancies = requests.get(f'https://api.hh.ru/vacancies/',
                                     params={'area': 113, 'text': keyword, 'per_page': word_count}).json()
            vacancies_list.extend([self.get_vacancy_by_id(i['id']) for i in vacancies['items']])
        return vacancies_list

    def get_vacancies_with_filters(self, keywords=None, salary=None, word_count=None):
        vacancies_list = []
        vacancies = requests.get(f'https://api.hh.ru/vacancies/',
                                 params={'area': 113, 'salary_from': salary, 'only_with_salary': True,
                                         'text': keywords, 'per_page': word_count}).json()
        vacancies_list.extend([self.get_vacancy_by_id(i['id']) for i in vacancies['items']])
        return vacancies_list

    def get_all_employers_vacancy(self, employer_id):
        response = requests.get(f'https://api.hh.ru/vacancies?employer_id={employer_id}',
                                params={'area': 113, 'only_with_salary': True, 'per_page': 100}).json()
        return [self.get_vacancy_by_id(i['id']) for i in response['items']]

    def get_employers_list(self, name):
        response = requests.get(f'https://api.hh.ru/employers',
                                params={'area': 113, 'text': name,
                                        'per_page': 100, 'only_with_vacancies': True}).json()
        return [self.get_employer_info(i['id']) for i in response['items']]

    @staticmethod
    def get_employer_info(employer_id):
        response = requests.get(f'https://api.hh.ru/employers/{employer_id}').json()
        return Employer(response['id'], response['name'], response['site_url'],
                        response['alternate_url'], response['description'], response['vacancies_url'],
                        response['open_vacancies'])

    @staticmethod
    def get_employer_by_vacancy_id(vacancy_id):
        response = requests.get(f'https://api.hh.ru/vacancies/{vacancy_id}').json()
        return response['employer']['id']
