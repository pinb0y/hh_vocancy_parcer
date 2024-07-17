from abc import ABC, abstractmethod

import requests
from requests import Response, JSONDecodeError

from src.exeption import HhApiException
from src.settings import HH_URL


class ParserApi(ABC):
    """
    Абстрактный класс для подключения и получения данных с API ресурса
    """

    @property
    @abstractmethod
    def url(self) -> str:
        """
        Свойство для получения базового URL для обращения к API
        """
        pass

    @abstractmethod
    def _get_response(self) -> Response:
        pass

    @abstractmethod
    def get_vacancies(self) -> list[dict]:
        pass

    @staticmethod
    @abstractmethod
    def _check_status(self) -> bool:
        pass


class HhParserApi(ParserApi):
    def __init__(self) -> None:
        self.__params = {
            "page": 0,
            "per_page": 100,
            "area": "113",
            "employer_id": ["9498120",
                            "5920492",
                            "64174",
                            "87021",
                            "15478",
                            "1375441",
                            "598471",
                            "633069",
                            "139",
                            "4496"]
        }
        self.__vacancies = []

    @property
    def url(self) -> str:
        return HH_URL

    def _get_response(self) -> Response:
        return requests.get(self.url, params=self.__params)

    def get_vacancies(self) -> None:
        response = self._get_response()
        is_allowed = self._check_status(response)
        if not is_allowed:
            raise HhApiException(f"Ошибка запроса данных. Status Code:{Response.status_code}")
        try:
            while self.__params.get("page") != 20:
                vacancies = response.json()["items"]
                self.__vacancies.extend(vacancies)
                self.__params["page"] += 1
        except JSONDecodeError:
            raise HhApiException("Ошибка получения данных")

    @property
    def vacancies(self):
        return self.__vacancies

    @staticmethod
    def _check_status(response: Response) -> bool:
        return response.status_code == 200
