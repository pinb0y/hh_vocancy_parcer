from src.classes.api import HhParserApi
from src.classes.company import Company
from src.classes.db_creator import DbCreator
from src.classes.db_manager import DbManager
from src.classes.vacancy import HhVacancy
from src.settings import config, DB_NAME


def main():
    """
    Основной цикл программы.
    :return: None
    """
    print("Подождите, пожалуйста\n")

    hh = HhParserApi()  # создание парсера
    hh.get_vacancies()  # Получение вакансий

    vacancies = HhVacancy.make_object_list(hh.vacancies)  # Создание списка объектов класса вакансия
    companies = Company.make_company_instances_list(hh.vacancies)  # Создание списка объектов класса компания

    hh_db = DbCreator(DB_NAME, config())  # Создание строителя базы данных
    hh_db.create_database()  # Создание Базы данных
    hh_db.create_tables()  # Создание шаблона таблиц
    hh_db.save_data_to_db(vacancies, companies)  # Заполнение Таблиц данными

    hh_db_manager = DbManager(DB_NAME, config())  # создание менеджера базы данных

    # Цикл пользовательского интерфейса
    while True:
        user_answer = input(f"[1] Вывести количество вакансий по компаниям\n"
                            f"[2] Вывести все вакансии\n"
                            f"[3] Вывести среднюю зарплату\n"
                            f"[4] Вывести все вакансии с зарплатой выше среднего\n"
                            f"[5] Вывести вакансии по ключевому запросу\n"
                            f"[0] Выйти из программы\n"
                            f"Выбери пункт меню: (введите цифру а потом клавишу ENTER) ")
        print()

        if user_answer == "1":
            for row in hh_db_manager.get_companies_and_vacancies_count():
                print(row)

        elif user_answer == "2":
            for row in hh_db_manager.get_all_vacancies():
                print(row)

        elif user_answer == "3":
            print(f'Средняя зарплата составляет {hh_db_manager.get_avg_salary()[0][0]} руб.')

        elif user_answer == "4":
            for row in hh_db_manager.get_vacancies_with_higher_salary():
                print(row)

        elif user_answer == "5":
            user_query = input("Введите слово для поиска\n")
            for row in hh_db_manager.get_vacancies_with_keyword(user_query):
                print(row)
        elif user_answer == "0":
            exit()

        print()

        input("Чтобы вернутся в меню нажмите Enter")


if __name__ == '__main__':
    main()
