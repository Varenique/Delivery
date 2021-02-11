class CustomError(Exception):
    def __init__(self, description: str, code: int, name: str):
        self.description = description
        self.code = code
        self.name = name

    def __str__(self):
        return self.name


class WrongIdError(CustomError):
    def __init__(self, description: str):
        super().__init__(name="Not Found", code=404, description=description)


class WrongPassword(CustomError):
    def __init__(self, description: str):
        super().__init__(name="Unauthorized", code=401, description=description)



