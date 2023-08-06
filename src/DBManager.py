import psycopg2
import os

class DBManager:
    def __init__(self, dbname, user, host):
        self.dbname = dbname
        self.user = user
        self.host = host
        self.conn = None
        self.connect_db()

    def connect_db(self):
        conn = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            host=self.host,
            password=os.environ['DBPassword']
        )
        self.conn = conn

    def add_employer(self, obj):
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO employers (employer_id, title, site_url, alt_url, vacancies_url) VALUES (%s, %s, %s, "
                    "%s, %s)",
                    (obj.employer_id, obj.title, obj.site_url, obj.alt_url, obj.vacancies_url)
                )
                self.conn.commit()
        except:
            self.conn.rollback()

    def add_vacancy(self, vacancy, employer_id):
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO vacancies (vacancy_id, employer_id, title, salary, alt_url) VALUES (%s, %s, %s, %s, "
                    "%s)",
                    (vacancy.vacancy_id, employer_id, vacancy.title, vacancy.salary, vacancy.url)
                )
                self.conn.commit()
        except:
            self.conn.rollback()

    def delete_vacancy(self, vacancy_id):
        try:
            with self.conn.cursor() as cur:
                cur.execute("DELETE FROM vacancies WHERE vacancy_id = %s", vacancy_id)
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(e)

    def get_companies_and_vacancies_count(self):
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "SELECT employers.employer_id, employers.title, COUNT(vacancies.vacancy_id) as vacancies_count "
                    "FROM employers "
                    "LEFT JOIN vacancies ON employers.employer_id = vacancies.employer_id "
                    "GROUP BY employers.employer_id"
                )
                results = cur.fetchall()
                return results
        except Exception as e:
            print(e)
            return []

    def get_all_vacancies(self):
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "SELECT employers.title as company_name, "
                    "vacancies.title  , vacancies.salary, vacancies.alt_url "
                    "FROM employers "
                    "INNER JOIN vacancies ON employers.employer_id = vacancies.employer_id"
                )
                results = cur.fetchall()
                return results
        except Exception as e:
            print(e)
            return []

    def get_avg_salary(self):
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "SELECT AVG(salary) as average_salary FROM vacancies"
                )
                result = cur.fetchone()
                return result[0] if result and result[0] is not None else 0
        except Exception as e:
            print(e)
            return 0

    def get_vacancies_with_higher_salary(self):
        higher_salary_vac = []
        avg_salary = self.get_avg_salary()
        for vacancy in self.get_all_vacancies():
            if vacancy[2] > avg_salary:
                higher_salary_vac.append(vacancy)
        return higher_salary_vac

    def get_vacancies_with_keyword(self, keyword):
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "SELECT employers.title as company_name, "
                    "vacancies.title as vacancy_title, vacancies.salary, vacancies.alt_url "
                    "FROM employers "
                    "INNER JOIN vacancies ON employers.employer_id = vacancies.employer_id "
                    "WHERE LOWER(vacancies.title) LIKE %s",
                    (f"%{keyword.lower()}%",)
                )
                results = cur.fetchall()
                return results
        except Exception as e:
            print(e)
            return []
