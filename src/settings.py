import pathlib
from configparser import ConfigParser

HH_URL = "https://api.hh.ru/vacancies"

ROOT_PATH = pathlib.Path(__file__).parent.parent

DATA_PATH = ROOT_PATH.joinpath("data")

DATABASE_PATH = DATA_PATH.joinpath("database.ini")

# путь к JSON файлу с вакансиями
VACANCIES_JSON_PATH = DATA_PATH.joinpath("vacancies.json")


def config(filename=DATABASE_PATH, section="postgresql"):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            "Section {0} is not found in the {1} file.".format(section, filename))

    return db
