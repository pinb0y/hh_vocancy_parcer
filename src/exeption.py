class ApiException(Exception):
    def __init__(self, massage):
        self.massage = massage
        super().__init__(self, massage)


class HhApiException(ApiException):
    pass
