class Student:
    def __init__(self, name, age):
     self.name = name
     self.age = age 

     def introduce (self):
        print("my name ", self.name)
        print("my age", self.age)

s1 = Student("vansh", 21)
s1.introduce()