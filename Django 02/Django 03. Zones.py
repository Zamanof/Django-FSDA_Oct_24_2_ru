# LEGB
# Local
# Enclosing
# Global
# Built-in

from math import pi as PI

print(f"built-in PI = {PI}")


def foo():
    # global PI
    PI = "Salam"
    def bar():
        # nonlocal PI
        PI = True
        print(f"Local PI = {PI}")
    bar()
    print(f"Enclosing PI = {PI}")


PI = 3.89
foo()
print(f"Global PI = {PI}")


# Closure, Generators, Decorators
