import psycopg2

from src.classes.company import Company
from src.classes.vacancy import HhVacancy


class DbCreator:

    def __init__(self, db_name, params):
        self.__database_name = db_name
        self.__params = params

    def create_database(self) -> None:
        conn = psycopg2.connect(dbname="postgres", **self.__params)
        conn.autocommit = True

        with conn.cursor() as cursor:
            cursor.execute(f'DROP DATABASE IF EXISTS {self.__database_name}')
            cursor.execute(f'CREATE DATABASE {self.__database_name}')

        conn.close()

    def create_tables(self):
        with psycopg2.connect(dbname=self.__database_name, **self.__params) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                            CREATE TABLE companies (
                                company_id INT PRIMARY KEY,
                                name VARCHAR(200) NOT NULL,
                                URL VARCHAR(100)
                            )
                        """)

            with conn.cursor() as cursor:
                cursor.execute("""
                            CREATE TABLE vacancies (
                                vacancy_id INT PRIMARY KEY,
                                company_id INT REFERENCES companies(company_id),
                                name VARCHAR(200) NOT NULL,
                                city VARCHAR(50),
                                URL VARCHAR(100),
                                salary_from INT,
                                salary_to INT,
                                requirements TEXT
                            )
                        """)
        conn.close()

    def save_data_to_db(self, vacancies: list[HhVacancy], companies: list[Company]):
        """Сохранение данных о вакансиях и компаниях в базу данных."""

        with psycopg2.connect(dbname=self.__database_name, **self.__params) as conn:
            with conn.cursor() as cur:
                for company in companies:
                    cur.execute(
                        """
                        INSERT INTO companies (company_id, name, URL)
                        VALUES (%s, %s, %s)
                        """,
                        (company.company_id, company.company_name, company.url)
                    )
                for vacancy in vacancies:
                    cur.execute(
                        """
                        INSERT INTO vacancies (vacancy_id, company_id, name, city, URL, 
                        salary_from, salary_to, requirements)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        (vacancy.vacancy_id, vacancy.company_id, vacancy.name, vacancy.city, vacancy.link,
                         vacancy.salary_from, vacancy.salary_to, vacancy.requirements)
                    )

        conn.close()
