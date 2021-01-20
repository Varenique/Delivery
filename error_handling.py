class CustomError(Exception):
    def __init__(self, description: str, status_code: int, name: str):
        self.description = description
        self.status_code = status_code
        self.name = name

    def __str__(self):
        return self.name


class ValidationError(CustomError):
    def __init__(self, description: str):
        super().__init__(name="Bad request", status_code=400, description=description)


class WrongIdError(CustomError):
    def __init__(self, description: str):
        super().__init__(name="Not Found", status_code=404, description=description)



