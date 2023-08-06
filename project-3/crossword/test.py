choice = {'first': 5, 'second': 2, 'third': 8, 'fourth': 1, 'fifth': 2, 'sixth': 9}

output = sorted(choice, key= lambda x: choice[x])

print(output)