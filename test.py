from new.cards import *
a = [1, 2, 3]
b = [4, 5, 6]

for x in (*a, b):
    print(x)