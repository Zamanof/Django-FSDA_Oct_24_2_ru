# Lambda expressions

# pure functions

# def add(a:int, b:int)-> int:
#     return a + b


def filter_negative(lst: list)-> list:
    negatives = []
    for item in lst:
        if item < 0:
            negatives.append(item)
    return negatives


def my_filter(lst: list, predicate)-> list:
    filtered = []
    for item in lst:
        if predicate(item):
            filtered.append(item)
    return filtered


def isNegative(item: int)-> bool:
    return item < 0

'''
def isNegative(item: int)-> bool:
    return item < 0
    
lambda x: item < 0
'''

def isPositive(item: int)-> bool:
    return item > 0

'''
def isPositive(item: int)-> bool:
    return item < 0

lambda x: item > 0
'''

lst = [56, -45, 9, 78, -58, 93, -1, 0]

# new_lst = filter_negative(lst)
# new_lst = my_filter(lst, isPositive)
new_lst = my_filter(lst, lambda x: x<0)
print(new_lst)





