import re
from html import unescape


class Employer:
    def __init__(self, employer_id: int, title: str, site_url, alt_url, description, vacancies_url, open_vacancies):
        """
        Конструктор класса Vacancy.
        """
        self.employer_id = employer_id
        self.title = title
        self.site_url = site_url
        self.alt_url = alt_url
        self.description = Employer.format_description(description)
        self.vacancies_url = vacancies_url
        self.open_vacancies = open_vacancies

    @classmethod
    def format_description(cls, text):
        """
        Форматирует описание работодателя, удаляя HTML-теги и декодируя спецсимволы.
        """
        try:
            text = re.sub('<.*?>', '', text)
            text = unescape(text)
            return text.strip()
        except:
            return 'Описание отсутствует'

    def __str__(self):
        """
        Возвращает строковое представление объекта вакансии.
        """
        return str(
            f"ID:{self.employer_id} {self.title}\nСайт: {self.site_url} \n{self.alt_url}\nОткрытых вакансий:"
            f"{self.open_vacancies} \n{self.description}")

    def to_dict(self):
        """
        Преобразует объект вакансии в словарь.
        """
        return {
            'employer_id': self.employer_id,
            'site_url': self.site_url,
            'title': self.title,
            'description': self.description,
            'vacancies_url': self.vacancies_url
        }

    @classmethod
    def from_dict(cls, data):
        """
        Создает объект вакансии из словаря.
        """
        return cls(
            data['employer_id'],
            data['site_url'],
            data['title'],
            data['description'],
            data['vacancies_url']
        )
