class Location:
    def __init__(self, name, country):
        self.name = name
        self.country = country
    
    def myLocation(self):
        print("Hi, my name is " + self.name + " and I live in " +
        self.country + ".")


loc = Location("Santiago", "Argentina")
print(loc.name)
print(loc.country)
print(type(loc))

loc1 = Location("Tomas", "Portugal")
loc1.myLocation()

loc2 = Location("Ying", "China")
loc3 = Location("Amare", "Kenya")

loc2.myLocation()
loc3.myLocation()

your_loc = Location("Santiago", "Argentina")
your_loc.myLocation()

