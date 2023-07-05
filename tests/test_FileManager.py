import pytest
import json
from src.vacancy import Vacancy
from src.WorkWithJSON import JSONVacancyFileManager


@pytest.fixture
def vacancy_file(tmp_path):
    file_path = tmp_path / "vacancies.json"
    return file_path


@pytest.fixture
def vacancy_manager(vacancy_file):
    return JSONVacancyFileManager(str(vacancy_file))


class TestJSONVacancyFileManager:
    def test_add_vacancy_adds_vacancy_to_file(self, vacancy_manager, vacancy_file):
        vacancy = Vacancy(1, "http://example.com", "Job Title", 5000, "Description", "Service")
        vacancy_manager.add_vacancy(vacancy)

        with open(vacancy_file) as file:
            data = json.load(file)
            assert len(data) == 1
            assert data[0]['vacancy_id'] == 1

    def test_delete_vacancy_deletes_vacancy_from_file(self, vacancy_manager, vacancy_file):
        vacancy1 = Vacancy(1, "http://example.com", "Job Title 1", 5000, "Description 1", "Service 1")
        vacancy2 = Vacancy(2, "http://example.com", "Job Title 2", 6000, "Description 2", "Service 2")

        vacancy_manager.add_vacancy(vacancy1)
        vacancy_manager.add_vacancy(vacancy2)
        vacancy_manager.delete_vacancy(1)

        with open(vacancy_file) as file:
            data = json.load(file)
            assert len(data) == 1
            assert data[0]['vacancy_id'] == 2

    def test_save_vacancies_to_file_saves_vacancies_to_file(self, vacancy_manager, vacancy_file):
        vacancies = [
            {'vacancy_id': 1, 'url': 'http://example.com', 'title': 'Job Title 1',
             'salary': 5000, 'description': 'Description 1', 'service': 'Service 1'},
            {'vacancy_id': 2, 'url': 'http://example.com', 'title': 'Job Title 2',
             'salary': 6000, 'description': 'Description 2', 'service': 'Service 2'}
        ]
        vacancy_manager.save_vacancies_to_file(vacancies)

        with open(vacancy_file) as file:
            data = json.load(file)
            assert data == vacancies

    def test_load_vacancies_from_file_loads_vacancies_from_file(self, vacancy_manager, vacancy_file):
        vacancies = [
            {'vacancy_id': 1, 'url': 'http://example.com', 'title': 'Job Title 1',
             'salary': 5000, 'description': 'Description 1', 'service': 'Service 1'},
            {'vacancy_id': 2, 'url': 'http://example.com', 'title': 'Job Title 2',
             'salary': 6000, 'description': 'Description 2', 'service': 'Service 2'}
        ]
        with open(vacancy_file, 'w') as file:
            json.dump(vacancies, file)

        loaded_vacancies = vacancy_manager.load_vacancies_from_file()
        assert loaded_vacancies == vacancies

    def test_get_vacancies_by_salary(self, vacancy_manager, vacancy_file):
        vacancy1 = Vacancy(1, "http://example.com", "Job Title 1", 5000, "Description 1", "Service 1")
        vacancy2 = Vacancy(2, "http://example.com", "Job Title 2", 5000, "Description 2", "Service 2")
        vacancy3 = Vacancy(3, "http://example.com", "Job Title 3", 6000, "Description 3", "Service 3")

        vacancy_manager.add_vacancy(vacancy1)
        vacancy_manager.add_vacancy(vacancy2)
        vacancy_manager.add_vacancy(vacancy3)

        filtered_vacancies = vacancy_manager.get_vacancies_by_salary(5000)
        assert len(filtered_vacancies) == 2
        assert filtered_vacancies[0].vacancy_id == 1
        assert filtered_vacancies[1].vacancy_id == 2

    def test_get_vacancies_by_keywords(self, vacancy_manager, vacancy_file):
        vacancy1 = Vacancy(1, "http://example.com", "Job Title 1", 5000, "Description with Python", "Service 1")
        vacancy2 = Vacancy(2, "http://example.com", "Job Title 2", 6000, "Description with Java", "Service 2")
        vacancy3 = Vacancy(3, "http://example.com", "Job Title 3", 7000, "Description with C++", "Service 3")

        vacancy_manager.add_vacancy(vacancy1)
        vacancy_manager.add_vacancy(vacancy2)
        vacancy_manager.add_vacancy(vacancy3)

        filtered_vacancies = vacancy_manager.get_vacancies_by_keywords(["python", "java"])
        assert len(filtered_vacancies) == 2
        assert filtered_vacancies[0].vacancy_id == 1
        assert filtered_vacancies[1].vacancy_id == 2

    def test_get_vacancies_by_salary_and_keywords(self, vacancy_manager, vacancy_file):
        vacancy1 = Vacancy(1, "http://example.com", "Job Title 1", 5000, "Description with Python", "HH")
        vacancy2 = Vacancy(2, "http://example.com", "Job Title 2", 6000, "Description with Java", "HH")
        vacancy3 = Vacancy(3, "http://example.com", "Job Title 3", 7000, "Description with C++", "SJ")

        vacancy_manager.add_vacancy(vacancy1)
        vacancy_manager.add_vacancy(vacancy2)
        vacancy_manager.add_vacancy(vacancy3)

        filtered_vacancies = vacancy_manager.get_vacancies_by_salary_and_keywords(5000, ["python"])
        assert len(filtered_vacancies) == 1
        assert filtered_vacancies[0].vacancy_id == 1