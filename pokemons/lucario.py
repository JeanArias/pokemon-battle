from pokemon import Pokemon

class Lucario(Pokemon):

    def __init__(self):
        super().__init__(
            "Lucario",
            "Lucha/Acero",
            250,
            202,
            130,
            211
        )

        self.imagen = (
                            "https://img.pokemondb.net/"
                            "sprites/sword-shield/normal/lucario.png"
                        )
       
    def atacar(self):
        print("Lucario usa Esfera Aural")
        return super().atacar() + 40