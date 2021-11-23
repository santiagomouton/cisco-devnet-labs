file = open("devices.txt", "a")
while(True):
    element = input("Enter a device name: ")
    if element == "exit":
        print("All done!")
        break
    file.write(element + "\n")