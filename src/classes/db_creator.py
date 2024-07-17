import psycopg2

from src.settings import config


class DbCreator:

    def __init__(self, db_name, params):
        self.__database_name = db_name
        self.__params = params

    def create_database(self) -> None:
        conn = psycopg2.connect(dbname="postgres", **self.__params)
        conn.autocommit = True

        with conn.cursor() as cursor:
            cursor.execute(f'DROP DATABASE {self.__database_name}')
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


if __name__ == "__main__":
    emp_base = DbCreator("hh", config())
    emp_base.create_database()
    emp_base.create_tables()