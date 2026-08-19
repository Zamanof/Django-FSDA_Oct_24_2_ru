# generators
# yield

# numbers = [i for i in range(10)]
# numbers1 = (i for i in range(10))
#
# # print(numbers)
# print(next(numbers1))
# print(next(numbers1))
# print(next(numbers1))
# print(next(numbers1))
# print(next(numbers1))
# print(next(numbers1))
# print(next(numbers1))
# print(next(numbers1))
# print(next(numbers1))
# print(next(numbers1))

# import datetime
#
# def infinite_days(start=None):
#     if start is None:
#         start = datetime.date.today()
#     while True:
#         yield start
#         start += datetime.timedelta(days=1)
#
# days = infinite_days()
#
# print(next(days))
# print(next(days))
# print(next(days))
# print(next(days))
# print(next(days))


def read_file_lines(path:str):
    with open(path, encoding="utf-8") as f:
        for l in f:
            yield l.strip()


for line in read_file_lines('students.txt'):
    input()
    print(line)


'''
Основные концепции
    1. Ленивость
    2. Экономия памяти
    3. Состояние генератора
    4. Одноразовость
'''