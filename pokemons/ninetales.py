from pokemon import Pokemon


class Ninetales(Pokemon):

    def __init__(self):
        super().__init__(
            "Ninetales", 
            "Fuego", 
            256, 
            141, 
            139, 
            184
            )
        self.imagen = (
            "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/38.png"
        )

    def atacar(self):
        print("¡Ninetales usa Lanzallamas!")
        return super().atacar() + 25