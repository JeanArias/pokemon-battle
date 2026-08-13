from pokemon import Pokemon

class Tentacruel(Pokemon):
    def __init__(self):
        super().__init__(
            "Tentacruel",
            "Water/Poison",
            270,
            130,
            121,
            148)

        self.imagen = (
                           "https://img.pokemondb.net/sprites/red-blue/normal/tentacruel.png"
                        )
    
    def atacar(self):
        print("Tentacruel usa tentaculos")
        return super().atacar()+10