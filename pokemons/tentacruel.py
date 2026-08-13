from pokemon import Pokemon

class Tentacruel(Pokemon):
    def __init__(self, nombre, tipo, vida, ataque, defensa, velocidad):
        super().__init__(
            "Tentacruel",
            "Water/Poison",
            80,
            70,
            65,
            100)
        self.imagen = (
            "https://img.pokemondb.net/artwork/tentacruel.jpg"
        )
        
    def atacar(self):
        print("Tentacruel usa tentaculos")
        return super().atacar()+10