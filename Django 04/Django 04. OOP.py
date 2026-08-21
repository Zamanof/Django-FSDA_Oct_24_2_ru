class Human:
    # name = "Nadir"
    # surname = "Zamanov"
    __count = 0
    def __init__(self, name, surname, age):
        self.name = name            # public
        self._surname = surname     # protected
        self.__age = age            # private
        Human.__count += 1

    def show_info(self):
        print(f"Name: {self.name}. Surname: {self._surname}. Age: {self.__age}")

    @staticmethod
    def get_count():
        return Human.__count

    @classmethod
    def show_count(cls):
        return cls.__count

human = Human("Nadir", "Zamanov", 45)
# print(human.count)
# print(Human.count)
human1 = Human("Ridan", "Vonamaz", 54)
# print(human1.count)
# print(human.count)
# print(Human.count)

# print(human._surname)
# print(human.__age)
# human.show_info()
# human1.show_info()
# print(Human.get_count())



