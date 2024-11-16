from dataclasses import dataclass


@dataclass
class Apartment:
    title: str
    link: str
    rooms: int
    city: str
    district: str
    price: int
    date: str
    area: int
