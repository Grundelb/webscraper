class Apartment:
    def __init__(self, title, link, rooms, city, district, price):
        self.title = title
        self.link = link
        self.rooms = rooms
        self.city = city
        self.district = district
        self.price = price

    def __str__(self):
        return f"\ntitle: {self.title}\ncity: {self.city}\ndistrict: {self.district}\nprice: {self.price}" \
               f"\nrooms: {self.rooms}"

    __repr__ = __str__
