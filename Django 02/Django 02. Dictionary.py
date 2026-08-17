# dct = {}
# dct1 = dict()
#
# print(type(dct))
# print(type(dct1))

dct = {
    "key": "Value",
    5: [25, 64],
    25.8: 2.66,
    True: "Salam",
    (2, 5): "Saqol"
    }

print(dct)
print(dct[(2, 5)])

# print(dct.keys())
# print(dct.values())
# print(dct.items())

for i in dct.keys():
    print(f"{i}: {dct[i]}")

print()

for i in dct.values():
    print(f"{i}")

print()

for key, value in dct.items():
    print(f"{key}: {value}")