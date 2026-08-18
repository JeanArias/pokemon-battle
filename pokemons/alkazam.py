from pokemon import Pokemon

class Alakazam(Pokemon):
    def __init__(self):
        super().__init__(
            "Alakazam",   # Nombre del Pokémon
            "Psychic",           # Tipo(s)
            55,               # HP (Vida)
            50,               # Attack (Ataque)
            45,               # Defense (Defensa)
            120               # Speed (Velocidad)
        )

    def atacar(self):
        print("¡Alakazam usa Magic Guard!")
        return super().atacar() + 10