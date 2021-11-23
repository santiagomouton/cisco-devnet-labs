items = []
file = open("devices.txt","r")
for line in file:
    items.append(line.strip())
file.close()
print(items)