import json
from src.vacancy import Vacancy
from abc import ABC, abstractmethod


class VacancyFileManager(ABC):
    @abstractmethod
    def add_vacancy(self, vacancy):
        """
        Добавляет вакансию в файл.
        """
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy_id):
        """
        Удаляет вакансию из файла по идентификатору.
        """
        pass

    @abstractmethod
    def save_vacancies_to_file(self, vacancies):
        """
        Сохраняет список вакансий в файл.
        """
        pass

    @abstractmethod
    def load_vacancies_from_file(self):
        """
        Загружает список вакансий из файла.
        """
        pass

    @abstractmethod
    def get_vacancies_by_salary(self, salary):
        """
        Возвращает список вакансий с указанной зарплатой.
        """
        pass

    @abstractmethod
    def get_vacancies_by_keywords(self, keywords):
        """
        Возвращает список вакансий, содержащих указанные ключевые слова в заголовке или описании.
        """
        pass

    @abstractmethod
    def get_vacancies_by_salary_and_keywords(self, salary, keywords):
        """
        Возвращает список вакансий с указанной зарплатой и содержащих указанные ключевые слова в заголовке или описании.
        """
        pass


class JSONVacancyFileManager(VacancyFileManager):
    def __init__(self, filename):
        self.filename = filename

    def add_vacancy(self, vacancy):
        vacancies = self.load_vacancies_from_file()
        vacancies.append(vacancy.to_dict())
        self.save_vacancies_to_file(vacancies)

    def delete_vacancy(self, vacancy_id):
        vacancies = self.load_vacancies_from_file()
        vacancies = [vacancy for vacancy in vacancies if vacancy['vacancy_id'] != vacancy_id]
        self.save_vacancies_to_file(vacancies)

    def save_vacancies_to_file(self, vacancies):
        with open(self.filename, 'w') as file:
            json.dump(vacancies, file)

    def load_vacancies_from_file(self):
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            return []

    def get_vacancies_by_salary(self, salary):
        vacancies = self.load_vacancies_from_file()
        filtered_vacancies = [Vacancy.from_dict(vacancy) for vacancy in vacancies if vacancy['salary'] == salary]
        return filtered_vacancies

    def get_vacancies_by_keywords(self, keywords):
        vacancies = self.load_vacancies_from_file()
        filtered_vacancies = []
        for vacancy in vacancies:
            title = vacancy['title']
            description = vacancy['description']
            if any(keyword in title.lower() or keyword in description.lower() for keyword in keywords):
                filtered_vacancies.append(Vacancy.from_dict(vacancy))
        return filtered_vacancies

    def get_vacancies_by_salary_and_keywords(self, salary, keywords):
        vacancies = self.load_vacancies_from_file()
        filtered_vacancies = []
        for vacancy in vacancies:
            vacancy_salary = vacancy['salary']
            title = vacancy['title'].lower()
            description = vacancy['description'].lower()
            if vacancy_salary > salary - 1 and all(
                    keyword.lower() in title or keyword.lower() in description for keyword in keywords):
                filtered_vacancies.append(Vacancy.from_dict(vacancy))
        return filtered_vacancies
