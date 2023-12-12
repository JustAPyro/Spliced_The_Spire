thing = False


def generator():
    while True:
        if thing:
            yield 'donuts'
        else:
            yield 'fried ice cream'


gen = generator()

for _ in range(10):
    print(next(gen))