import re
from html import unescape


class Vacancy:
    def __init__(self, vacancy_id: int, url: str, title: str, salary, description: str, service: str):
        """
        Конструктор класса Vacancy.
        """
        self.vacancy_id = vacancy_id
        self.url = url
        self.title = title
        self.salary = salary
        self.description = Vacancy.format_description(description)
        self.service = service

    @classmethod
    def format_description(cls, text):
        """
        Форматирует описание вакансии, удаляя HTML-теги и декодируя спецсимволы.
        """
        text = re.sub('<.*?>', '', text)
        text = unescape(text)
        return text.strip()

    def __str__(self):
        """
        Возвращает строковое представление объекта вакансии.
        """
        return str(f"ID:{self.vacancy_id} {self.title}\nЗ/П: {self.salary} {self.url}\n{self.description}")

    @classmethod
    def __verify_data(cls, other):
        """
        Вспомогательный метод для сравнения объекта вакансии с другим объектом
        или с зарплатой другого объекта вакансии.
        """
        return other if isinstance(other, int) else other.salary

    def __lt__(self, other):
        """
        Метод для определения отношения "меньше" с другим объектом вакансии
        или с зарплатой другого объекта вакансии.
        """
        sc = self.__verify_data(other)
        return self.salary < sc

    def __eq__(self, other):
        """
        Метод для определения отношения "равно" с другим объектом вакансии
        или с зарплатой другого объекта вакансии.
        """
        sc = self.__verify_data(other)
        return self.salary == sc

    def to_dict(self):
        """
        Преобразует объект вакансии в словарь.
        """
        return {
            'vacancy_id': self.vacancy_id,
            'url': self.url,
            'title': self.title,
            'salary': self.salary,
            'description': self.description,
            'service': self.service
        }

    @classmethod
    def from_dict(cls, data):
        """
        Создает объект вакансии из словаря.
        """
        return cls(
            data['vacancy_id'],
            data['url'],
            data['title'],
            data['salary'],
            data['description'],
            data['service']
        )
