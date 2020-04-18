class Person(object):

    name = ""

    def __init__(self, name): 
        print("Person init called") 
        self.name = name 
          
  
class Athelete(Person): 

    speed = 0

    def __init__(self, speed): 
        print("Athelete init called") 
        self.speed = speed 


atl = Athelete(10)
atl.name = "Dhruv Singla"
print(atl.name)