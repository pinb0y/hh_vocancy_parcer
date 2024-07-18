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
        """
        Абстрактный метод для подключения к api
        :return:
        """
        pass

    @abstractmethod
    def get_vacancies(self) -> list[dict]:
        """
        Абстрактный метод получения вакансий
        :return:
        """
        pass

    @staticmethod
    @abstractmethod
    def _check_status(response) -> bool:
        """
        Абстрактный метод проверки подключения
        :return: Тру или фолз в зависимости от статуса.
        """
        pass


class HhParserApi(ParserApi):
    """
    Класс для парсинга вакансий с сайта HeadHunter
    """
    def __init__(self) -> None:
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.__params = {
            "area": 113,
            "page": 0,
            "per_page": 100,
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
        """
        Свойство возвращающее ссылку для подключения
        :return: адрес API HH
        """
        return HH_URL

    def _get_response(self) -> Response:
        """
        Подключение к API HH
        :return: Возвращает подключение
        """
        return requests.get(self.url, headers=self.headers, params=self.__params)

    def get_vacancies(self) -> None:
        """
        Метод записывает в свойства объекта список словарей с вакансиями
        :return: None
        """
        response = self._get_response()
        is_allowed = self._check_status(response)
        if not is_allowed:
            raise HhApiException(f"Ошибка запроса данных. Status Code:{Response.status_code}")
        try:
            while self.__params.get("page") != 20:
                response = self._get_response()
                vacancies = response.json()["items"]
                self.__vacancies.extend(vacancies)
                self.__params["page"] += 1
        except JSONDecodeError:
            raise HhApiException("Ошибка получения данных")

    @property
    def vacancies(self):
        """
        Геттер списка вакансий
        :return:
        """
        return self.__vacancies

    @staticmethod
    def _check_status(response: Response) -> bool:
        """
        Метод проверяющий подключение
        :return: тру или фолз в зависимости от статуса
        """
        return response.status_code == 200
