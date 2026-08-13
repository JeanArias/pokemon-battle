from pokemon import Pokemon

class Lucario(Pokemon):

    def __init__(self):
        super().__init__(
            "Lucario",
            "Lucha/Acero",
            110,
            30,
            20,
            25
        )

    def atacar(self):
        print("Lucario usa Esfera Aural")
        return super().atacar() + 10