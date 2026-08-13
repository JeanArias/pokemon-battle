from pokemon import Pokemon

class Pikachu(Pokemon):
    
    def __init__(self):
        super().__init__(
            "Pikachu", 
            "Electrico", 
            180, 
            103, 
            76, 
            166
            )
        self.imagen = (
            "https://img.pokemondb.net/"
            "sprites/red-blue/normal/pikachu.png"
        )

    def atacar(self):
        print("Pikachu usa Chispa")
        return super().atacar()+10