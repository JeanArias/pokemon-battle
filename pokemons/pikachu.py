from pokemon import Pokemon

class Pikachu(Pokemon):
    def __init__(self):
        super().__init__(
            "Pikachu", 
            "Electrico", 
            100, 
            25, 
            8, 
            18
            )

    def atacar(self):
        print("Pikachu usa Impactrueno")
        return super().atacar()+8