class Company:
    """
    Класс для создания объектов компаний
    """
    def __init__(self, company_id: str, company_name: str, url: str):
        self.company_id = int(company_id)
        self.company_name = company_name
        self.url = url

    @classmethod
    def make_company_instances_list(cls, data: list[dict]):
        """
        Класс метод создает список объектов класса компания
        :param data: список словарей с компаниями
        :return: список объектов компаний
        """
        company_list: list = []
        company_ids = set()
        for company in data:
            if company["employer"]["id"] not in company_ids:
                temp: Company = cls(
                    company_id=company["employer"]["id"],
                    url=company["employer"]["alternate_url"],
                    company_name=company["employer"]["name"])
                company_list.append(temp)
                company_ids.add(company["employer"]["id"])
        return company_list
