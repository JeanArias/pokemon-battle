from pokemon import Pokemon

class Charmander(Pokemon):

    def __init__(self):
        super().__init__(
            "Charmander",
             "Fuego",
              110, 
              24, 
              10, 
              15)
        self.imagen = (
            "https://img.pokemondb.net/"
            "sprites/red-blue/normal/charmander.png"
        )

    def atacar(self):
        print("Charmander usa Lanzallamas")
        return super().atacar()+10