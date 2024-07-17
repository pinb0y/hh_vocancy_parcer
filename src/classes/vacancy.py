class HhVacancy:
    """Класс для работы с вакансиями с сайта HeadHunter"""

    name: str
    link: str
    company: str
    city: str
    experience: str
    salary_from: int
    salary_to: int

    def __init__(self, vacancy_id: int, name: str, link: str, company: str, company_id: int, company_link: str,
                 city: str, experience: str, requirements: str, salary_from=0, salary_to=0):
        self.vacancy_id = vacancy_id
        self.name = name
        self.link = link
        self.company = company
        self.company_id = company_id
        self.company_link = company_link
        self.__salary_from = salary_from if salary_from else 0
        self.__salary_to = salary_to if salary_to else 0
        self.city = city
        self.experience = experience
        self.requirements = requirements

    def __str__(self) -> str:
        """Вывод данных для пользователя"""

        return ("----------------------------------------\n"
                f"Вакансия {self.name}, Опыт {self.experience}\n"
                f"Ссылка {self.link}\n"
                f"Город {self.city}, Компания {self.company}\n"
                f"Зарплата {self.salary_print()} руб.\n")

    def __lt__(self, other) -> bool:
        return self.__salary_from < other.__salary_from

    def __gt__(self, other) -> bool:
        return self.__salary_from > other.__salary_from

    def salary_print(self) -> str:
        """
        Корректный вывод зарплаты пользователю.
        1. Если указана "от".
        2. Если указана "до".
        3. Если указана "от" и "до".
        4. Зарплата не указана
        :return: Строка
        """

        if self.__salary_from and self.__salary_to:
            return f"от {self.__salary_from} до {self.__salary_to}"
        elif self.__salary_from and not self.__salary_to:
            return f"от {self.__salary_from}"
        elif not self.__salary_from and self.__salary_to:
            return f"до {self.__salary_to}"
        else:
            return "Зарплата не указана"

    @classmethod
    def make_object_list(cls, vacancies: list[dict]) -> list:
        """
        Создает список объектов вакансий.
        :param vacancies: Список вакансий из JSON файла
        :return: Список объектов класса вакансия.
        """

        vacancies_list: list = []
        for vacancy in vacancies:
            temp: HhVacancy = cls(
                vacancy_id=vacancy["id"],
                name=vacancy["name"],
                link=vacancy["alternate_url"],
                company_id=vacancy["employer"]["id"],
                company_link=vacancy["employer"]["alternate_url"],
                company=vacancy["employer"]["name"],
                salary_from=vacancy["salary"]["from"] if vacancy["salary"] else 0,
                salary_to=vacancy["salary"]["to"] if vacancy["salary"] else 0,
                city=vacancy["area"]["name"],
                experience=vacancy["experience"]["name"],
                requirements=vacancy["snippet"]["requirement"]
            )
            vacancies_list.append(temp)
        return vacancies_list

    @property
    def salary_from(self) -> int:
        """Геттер зарплаты "от"."""

        return self.__salary_from
