import pytest
from html import unescape
from src.vacancy import Vacancy

class TestVacancy:
    def test_format_description_removes_html_tags(self):
        text = "<p>This is a <b>bold</b> text.</p>"
        expected = "This is a bold text."
        assert Vacancy.format_description(text) == expected

    def test_format_description_decodes_special_characters(self):
        text = "This is a &lt;bold&gt; text."
        expected = "This is a <bold> text."
        assert Vacancy.format_description(text) == expected

    def test_format_description_strips_whitespace(self):
        text = "   This is a description with whitespace.   "
        expected = "This is a description with whitespace."
        assert Vacancy.format_description(text) == expected

    def test_str_returns_string_representation_of_vacancy(self):
        vacancy = Vacancy(1, "http://example.com", "Job Title", 5000, "Description", "Service")
        expected = "ID:1 Job Title\nЗ/П: 5000 http://example.com\nDescription"
        assert str(vacancy) == expected

    def test_lt_compares_vacancy_salary_with_other_vacancy_salary(self):
        vacancy1 = Vacancy(1, "http://example.com", "Job Title 1", 5000, "Description 1", "Service 1")
        vacancy2 = Vacancy(2, "http://example.com", "Job Title 2", 6000, "Description 2", "Service 2")
        assert vacancy1 < vacancy2

    def test_lt_compares_vacancy_salary_with_integer_salary(self):
        vacancy = Vacancy(1, "http://example.com", "Job Title", 5000, "Description", "Service")
        assert vacancy < 6000

    def test_eq_compares_vacancy_salary_with_other_vacancy_salary(self):
        vacancy1 = Vacancy(1, "http://example.com", "Job Title 1", 5000, "Description 1", "Service 1")
        vacancy2 = Vacancy(2, "http://example.com", "Job Title 2", 5000, "Description 2", "Service 2")
        assert vacancy1 == vacancy2

    def test_eq_compares_vacancy_salary_with_integer_salary(self):
        vacancy = Vacancy(1, "http://example.com", "Job Title", 5000, "Description", "Service")
        assert vacancy == 5000

    def test_to_dict_returns_vacancy_as_dictionary(self):
        vacancy = Vacancy(1, "http://example.com", "Job Title", 5000, "Description", "Service")
        expected = {
            'vacancy_id': 1,
            'url': 'http://example.com',
            'title': 'Job Title',
            'salary': 5000,
            'description': 'Description',
            'service': 'Service'
        }
        assert vacancy.to_dict() == expected

    def test_from_dict_creates_vacancy_from_dictionary(self):
        data = {
            'vacancy_id': 1,
            'url': 'http://example.com',
            'title': 'Job Title',
            'salary': 5000,
            'description': 'Description',
            'service': 'Service'
        }
        vacancy = Vacancy.from_dict(data)
        assert vacancy.vacancy_id == 1
        assert vacancy.url == 'http://example.com'
        assert vacancy.title == 'Job Title'
        assert vacancy.salary == 5000
        assert vacancy.description == 'Description'
        assert vacancy.service == 'Service'
