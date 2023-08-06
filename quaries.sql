CREATE TABLE vacancies
(
	vacancy_id SERIAL PRIMARY KEY,
	employer_id INTEGER REFERENCES employers(employer_id),
	title varchar,
	salary INTEGER,
	alt_url varchar
);

CREATE TABLE employers
(
	employer_id SERIAL PRIMARY KEY,
	title varchar,
	site_url varchar,
	alt_url varchar,
	vacancies_url varchar
);