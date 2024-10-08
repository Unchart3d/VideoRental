class Customer:
    def __init__(self, firstName, lastName, address, phone, email):
        self.firstName = firstName
        self.lastName = lastName
        self.address = address
        self.phone = phone
        self.email = email
        
class Video:
    def __init__(self, name, year, director, rating, genre, rentalStatus):
        self.name = name
        self.year = year
        self.director = director
        self.rating = rating
        self.genre = genre
        self.rentalStatus = rentalStatus