# Decorators

# def decorator_function(original_function):
#     def wrapper_function(*args, **kwargs):
#         print("Some operations before")
#         print(args)
#         print(kwargs)
#         result = original_function(*args, **kwargs)
#         print(f"Function result = {result}")
#         print("Some operations after")
#         return result
#     return wrapper_function

# @decorator_function
# def my_function(numb1, numb2):
#     return numb1 + numb2
#
# @decorator_function
# def other_function(numb1, numb2, numb3):
#     return numb1 + numb2 - numb3
#
# # print(my_function(25, 65))
#
# other_function(25, 98, 2225)

# authorize example
# def is_authorize(login:str, password:str)-> bool:
#     return login == 'admin' and password == 'admin'
#
# def check_authorize(func):
#     def wrapper(*args, **kwargs):
#         if is_authorize(kwargs['login'], kwargs['password']):
#             print('User authorized')
#             return func(*args, *kwargs)
#         else:
#             raise Exception('401 Unauthorized')
#     return wrapper
#
# @check_authorize
# def do_something(login:str, password:str):
#     print("Do something")
#
#
# @check_authorize
# def add(numb1, numb2, login:str, password:str):
#     print(numb1 + numb2)
#
# # do_something(login='admin', password='adminq')
#
# add(25, 65, login='admin', password='admin')

# validation example


def validate_int_arguments(func):
    def wrapper(*args, **kwargs):
        for arg in [*args, *kwargs.values()]:
            if not isinstance(arg, int):
                raise TypeError(f"{str(type(arg))[7:-1]} object cannot be interpreted as an integer")
            return func(*args, **kwargs)
    return wrapper

@validate_int_arguments
def summ(left:int, right:int)->int:
    return left + right

@validate_int_arguments
def my_range(start:int, stop:int=None, step:int=1)-> list:
    lst = []
    if stop is None:
        stop = start
        start = 0
    while start < stop:
        lst.append(start)
        start += step
    return lst


# print(my_range('True'))

# print(summ(2.5, 5))

