class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def bark(self):
        print("Woof Woof!")
    
    def celebrateBirthday(self):
        self.age += 1
        print(f"Happy birthday, {self.name}!")
        
    def getInfo(self):
        return f"Dog's name: {self.name}, Age: {self.age}"
    
if __name__ == "__main__":
    my_dog = Dog("Dahlia", 2)
    my_dog.bark()
    my_dog.celebrateBirthday()
    print(my_dog.getInfo())
    
    
        