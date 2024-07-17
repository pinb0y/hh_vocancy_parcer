class HhVacancy:
    """Класс для работы с вакансиями с сайта HeadHunter"""

    def __init__(self, vacancy_id: int, name: str, link: str, company_id: int,
                 city: str, experience: str, requirements: str, salary_from=0, salary_to=0):
        self.vacancy_id = int(vacancy_id)
        self.name = name
        self.link = link
        self.company_id = int(company_id)
        self.__salary_from = salary_from if salary_from else None
        self.__salary_to = salary_to if salary_to else None
        self.city = city
        self.experience = experience
        self.requirements = requirements

    def __lt__(self, other) -> bool:
        return self.__salary_from < other.__salary_from

    def __gt__(self, other) -> bool:
        return self.__salary_from > other.__salary_from

    @classmethod
    def make_object_list(cls, vacancies: list[dict]) -> list:
        """
        Создает список объектов вакансий.
        :param vacancies: Список вакансий из JSON файла
        :return: Список объектов класса вакансия.
        """

        vacancies_list: list = []
        vacancy_ids = set()
        for vacancy in vacancies:
            if vacancy["id"] not in vacancy_ids:
                temp: HhVacancy = cls(
                    vacancy_id=vacancy["id"],
                    name=vacancy["name"],
                    link=vacancy["alternate_url"],
                    company_id=vacancy["employer"]["id"],
                    salary_from=vacancy["salary"]["from"] if vacancy["salary"] else 0,
                    salary_to=vacancy["salary"]["to"] if vacancy["salary"] else 0,
                    city=vacancy["area"]["name"],
                    experience=vacancy["experience"]["name"],
                    requirements=vacancy["snippet"]["requirement"])
                vacancies_list.append(temp)
                vacancy_ids.add(vacancy["id"])
        return vacancies_list

    @property
    def salary_from(self) -> int:
        """Геттер зарплаты "от"."""

        return self.__salary_from

    @property
    def salary_to(self) -> int:
        """Геттер зарплаты "до"."""

        return self.__salary_to
