from random import choices

thing = False


def generator():
    while True:
        if thing:
            yield 'donuts'
        else:
            yield 'fried ice cream'


x = choices(['a', 'b', 'c'],
            [10, 30, 60])

a = 0
b = 0
c = 0

for _ in range(10000):
    x = choices(['a', 'b', 'c'],
            [10, 30, 60])[0]
    print(x)
    if x == 'a':
        a += 1
    if x == 'b':
        b += 1
    if x == 'c':
        c += 1

print(a, b, c)


