# lst = []
# lst = list()

# print(type(lst))

# lst.append(5)
# lst.append(36)
# lst.append(2.36)
# print(lst)


list1 = [25, 69]
# list2 = list1       # shallow copy

# deep copy - v1
# list2 = []
# for i in list1:
#     list2.append(i)

# deep copy - v2
# list2 = list1.copy()

import copy
# deep copy - v3
# list2 = copy.deepcopy(list1)

# deep copy - v4
list2 = list1[:]

print(f"list1 = {list1}")
print(f"list2 = {list2}")

list2[0] = 294

print()

print(f"list1 = {list1}")   # [294, 69]
print(f"list2 = {list2}")   # [294, 69]
