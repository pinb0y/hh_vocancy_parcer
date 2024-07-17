from src.classes.api import HhParserApi
from src.classes.company import Company
from src.classes.db_creator import DbCreator
from src.classes.vacancy import HhVacancy
from src.settings import config


def main():
    hh = HhParserApi()
    hh.get_vacancies()
    vacancies = HhVacancy.make_object_list(hh.vacancies)
    companies = Company.make_company_instances_list(hh.vacancies)
    emp_base = DbCreator("hh", config())
    emp_base.create_database()
    emp_base.create_tables()
    emp_base.save_data_to_db(vacancies, companies)


if __name__ == '__main__':
    main()
