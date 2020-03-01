import random
print('Testing\n')

row = []
col = []

row.append(5)
col.append(4)

row.append(6)
col.append(7)

row.append(8)
col.append(9)

rand_index = random.randint(0,(len(row)-1))

print(rand_index)
print(row[rand_index])
print(col[rand_index])