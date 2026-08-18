from pokemon import Pokemon
class Jigglypuff(Pokemon):
    def __init__(self):
        super().__init__(
              "Jigglypuff",
              "Normal",
              115,
              45,
              20,
              20
              )
        self.imagen = (
            "https://imgpokemondb.net/"
            "sprites/red-blue/normal/jigglypuff.png"
        )

def atacar(self):
    print("Jigglypuff usa Canto")
    return super ().atacar()+10

