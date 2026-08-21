class Human:
    def __init__(self, name, surname, age):
        self.name = name                              # public
        self._surname = surname                       # protected
        self.__age = age if age > 0 else 0            # private

    def __repr__(self):
        return f'Human({self.name}, {self._surname}, {self.__age})'

    def __str__(self):
        return f'Human({self.name}, {self._surname}, {self.__age})'

    def __add__(self, other):
        return self.name + other.name

    def __eq__(self, other):
        return self.__age == other.__age




human = Human(name='Salam', surname='Zamanov', age=18)
human1 = Human(name='Nadir', surname='Salamov', age=18)
print(human == human1)
