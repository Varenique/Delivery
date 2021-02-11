from dataclasses import dataclass


@dataclass
class Restaurant:
    name: str = ""
    address: str = ""
    work_time: str = ""
    phone_number: str = ""
    id: str = ""


@dataclass
class User:
    login: str = ""
    password: str = ""
    name: str = ""
    phone_number: str = ""
    rights: str = ""
    id: str = ""
