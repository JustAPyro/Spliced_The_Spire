x = {1: 'one', 2: 'two'}

for i in list(x):
    if i == 1:
        x.pop(i)

print(x)
