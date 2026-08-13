from pokemon import Pokemon

class Charmander(Pokemon):

    def __init__(self):
        super().__init__(
            "Charmander",
             "Fuego",
              188, 
              95, 
              81, 
              121)

        self.imagen = (
            "https://img.pokemondb.net/"
            "sprites/red-blue/normal/charmander.png"
        )

    def atacar(self):
        print("Charmander usa Colmillo de fuego")
        return super().atacar()+13