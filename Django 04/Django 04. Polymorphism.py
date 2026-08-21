class Human:
    type = "Human"
    def __init__(self, name, surname, age):
        self.name = name                              # public
        self._surname = surname                       # protected
        self.__age = age if age > 0 else 0            # private

    def get_info(self):
        return f"Name: {self.name}. Surname: {self._surname}. Age: {self.__age}"

    @staticmethod
    def get_type_static_method():
        return Human.type

    @classmethod
    def get_type_class_method(cls):
        return cls.type

class Student(Human):
    type = "Student"
    def __init__(self, name, surname, age, group):
        super().__init__(name, surname, age)
        self.group = group

    def get_info(self):
        return f"{super().get_info()}. Group: {self.group}"


class Foo:
    def get_info(self):
        return "Salam"

class Other:
    def get_info(self):
        return "Hi"

student = Student("Nadir", "Zamanov", 1901, "FSDA_Oct_24_2_ru")
human = Human("Ali", "Aliyev", 25)
foo = Foo()
other = Other()
lst = [student, human, foo, other]

for item in lst:
    print(item.get_info())

# print(human.get_type_class_method())
# print(human.get_type_static_method())

# print(student.get_type_class_method())      # Human, Student
# print(student.get_type_static_method())     # Student, Human


# утиная типизация
