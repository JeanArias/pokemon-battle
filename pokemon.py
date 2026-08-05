import random


class Pokemon:

    def __init__(self, nombre, tipo, vida, ataque, defensa, velocidad):

        self.nombre = nombre
        self.tipo = tipo
        self.__vida = vida
        self.ataque = ataque
        self.defensa = defensa
        self.velocidad = velocidad

    @property
    def vida(self):
        return self.__vida

    def mostrar_estado(self):

        print(f"\n{self.nombre}")
        print(f"Tipo      : {self.tipo}")
        print(f"Vida      : {self.__vida}")
        print(f"Ataque    : {self.ataque}")
        print(f"Defensa   : {self.defensa}")
        print(f"Velocidad : {self.velocidad}")

    def atacar(self):

        daño = random.randint(
            self.ataque - 5,
            self.ataque + 5
        )

        return daño

    def recibir_daño(self, daño):

        daño_real = max(1, daño - self.defensa)

        self.__vida -= daño_real

        if self.__vida < 0:
            self.__vida = 0

        print(f"{self.nombre} recibe {daño_real} puntos de daño.")

    def esta_vivo(self):

        return self.__vida > 0

    def curar(self, puntos):

        self.__vida += puntos

        print(f"{self.nombre} recupera {puntos} puntos de vida.")