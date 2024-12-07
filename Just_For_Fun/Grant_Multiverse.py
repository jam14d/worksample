#Creating a person named Grant
#Multiple copies of him with different outfits


class Grant:
    def __init__(self, race, outfit):
        self.race = race
        self.outfit = outfit
    def describe(self):
        return f"A {self.race} man with a nice {self.outfit}."


class Multiverse:
    def __init__(self):
        self.clones = [] #this will hold all of the Grants

    def add_clones(self,clone):
        self.clones.append(clone)

    def list_clones(self):
        for i, clone in enumerate(self.clones):
            print(f"Grant Clone {i +1}: {clone.describe()}")

#Create some Grant Clones
Grant1 = Grant("Korean", "white crew-neck T-shirt, light blue jeans, white sneakers, black leather watch, aviator sunglasses, denim jacket.")
Grant2 = Grant("Korean", "floral print blouse, earth-tone maxi skirt, brown leather sandals, layered necklaces, wide-brim hat.")
Grant3 = Grant("Korean", "black graphic T-shirt, ripped skinny jeans, black combat boots, studded leather jacket, silver chain necklace")

#Create Multiverse of Grants
my_multiverse = Multiverse() 

#Add clones to the Multiverse
my_multiverse.add_clones(Grant1)
my_multiverse.add_clones(Grant2)
my_multiverse.add_clones(Grant3)


#List all Grants in Multiverse
my_multiverse.list_clones()
