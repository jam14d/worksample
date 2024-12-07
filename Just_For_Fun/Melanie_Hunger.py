

class Cat:
    def __init__ (self,name, emotions):
        self.name = name
        self.emotions = ["happy", "neutral", "annoyed", "sassy"]
    def feed (self):
        if self.hunger > 0:
            print(f"{self.name} is hungry. Hunger level is {self.hunger}")
    def mood (self):
        if self.hunger >=5:
            mood = slice(-1, None)


##IN PROGRESS