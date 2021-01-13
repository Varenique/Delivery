from flask import jsonify


class HandledError(Exception):
    def __init__(self, description: str, status_code: int, name: str):
        self.description = description
        self.status_code = status_code
        self.name = name

    def __str__(self):
        return self.description




