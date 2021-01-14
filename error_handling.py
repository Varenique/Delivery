class HandledError(Exception):
    def __init__(self, description: str, status_code: int, name: str):
        self.description = description
        self.status_code = status_code
        self.name = name

    def __str__(self):
        return self.name


class ValidationError(HandledError):
    name = "Bad request"
    status_code = 400

    def __init__(self, description: str):
        self.description = description

    def __str__(self):
        return self.name



