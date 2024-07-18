class ApiException(Exception):
    """
    Основной класс для исключений
    """
    def __init__(self, massage):
        self.massage = massage
        super().__init__(self, massage)


class HhApiException(ApiException):
    """
    Класс для исключений парсера HH
    """
    pass
