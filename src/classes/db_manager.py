import psycopg2


class DbManager:
    """
    Класс для управления базой данных
    """
    def __init__(self, db_name, params):
        self.__database_name = db_name
        self.__params = params

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        """
        with psycopg2.connect(dbname=self.__database_name, **self.__params) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                SELECT companies.name, COUNT(*) AS vacancies_count FROM companies
                JOIN vacancies USING (company_id)
                GROUP BY companies.name
                """)
                result = cursor.fetchall()
        conn.close()
        return result

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
        """
        with psycopg2.connect(dbname=self.__database_name, **self.__params) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                SELECT companies.name, vacancies.name, salary_from, salary_to, vacancies.URL FROM vacancies
                JOIN companies USING (company_id)
                """)
                result = cursor.fetchall()
        conn.close()
        return result

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям.
        """
        with psycopg2.connect(dbname=self.__database_name, **self.__params) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""SELECT CAST(AVG(salary_from) as INT) FROM vacancies""")
                result = cursor.fetchall()
        conn.close()
        return result

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """

        with psycopg2.connect(dbname=self.__database_name, **self.__params) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""SELECT * FROM vacancies
                WHERE salary_from > (SELECT AVG(salary_from) FROM vacancies)
                ORDER BY salary_from DESC
                """)
                result = cursor.fetchall()
        conn.close()
        return result

    def get_vacancies_with_keyword(self, keyword: str):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.
        """
        with psycopg2.connect(dbname=self.__database_name, **self.__params) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""SELECT * FROM vacancies
                       WHERE name LIKE '%{keyword}%' OR requirements LIKE '%{keyword}%'
                       ORDER BY salary_from DESC
                       """)
                result = cursor.fetchall()
        conn.close()
        return result
