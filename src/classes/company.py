class Company:
    def __init__(self, company_id, company_name, url):
        self.company_id = int(company_id)
        self.company_name = company_name
        self.url = url

    @classmethod
    def make_company_instances_list(cls, data):
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
