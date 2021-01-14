class CustomError(Exception):
    def __init__(self, description: str, status_code: int, name: str):
        self.description = description
        self.status_code = status_code
        self.name = name

    def __str__(self):
        return self.name


class ValidationError(CustomError):
    name = "Bad request"
    status_code = 400

    def __init__(self, description: str):
        self.description = description

    def __str__(self):
        return self.name


class WrongIdError(CustomError):
    name = "Not Found"
    status_code = 404

    def __init__(self, description: str):
        self.description = description

    def __str__(self):
        return self.name


