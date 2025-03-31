class Peoples(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return print(f"Name: {self.name}\nAge: {self.age}")

p1 = Peoples('Vlad', 18)
p1.__str__()