from pokemon import Pokemon

class Hunter(Pokemon):

    def __init__(self):
        super().__init__(
             "Hunter",
             "Fantasma",
              200, 
              94, 
              85, 
              175)

    def atacar(self):
        print("Hunter usa Garra siniestra")
        return super().atacar()+20
    
