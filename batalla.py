from eventos import aplicar_evento
import time


class Batalla:

    def __init__(self, pokemon1, pokemon2):

        self.pokemon1 = pokemon1
        self.pokemon2 = pokemon2

    # -------------------------

    def pausar(self):

        input("\n👉 Presione ENTER para continuar...")

    # -------------------------

    def mostrar_estados(self):

        print("\n==============================")

        self.pokemon1.mostrar_estado()

        print("------------------------------")

        self.pokemon2.mostrar_estado()

        print("==============================")

    # -------------------------

    def ejecutar_turno(self, atacante, defensor):

        print(f"\n🎯 Turno de {atacante.nombre}")

        time.sleep(1)

        evento = aplicar_evento(atacante, defensor)

        # -------------------------

        if evento == "dormido":

            print(f"\n😴 {atacante.nombre} está dormido.")

            print("Pierde el turno.")

            self.pausar()

            return

        # -------------------------

        if evento == "esquivar":

            print(f"\n🛡 {defensor.nombre} esquivó el ataque.")

            self.pausar()

            return

        # -------------------------

        daño = atacante.atacar()

        if evento == "critico":

            daño *= 2

            print("💥 ¡ATAQUE CRÍTICO!")

        defensor.recibir_daño(daño)

        self.pausar()

        self.mostrar_estados()

        self.pausar()

    # -------------------------

    def combatir(self):

        print("=" * 45)
        print("        ⚔️ POKÉMON BATTLE ⚔️")
        print("=" * 45)

        self.mostrar_estados()

        self.pausar()

        # Determinar quién comienza

        if self.pokemon1.velocidad >= self.pokemon2.velocidad:

            primero = self.pokemon1
            segundo = self.pokemon2

        else:

            primero = self.pokemon2
            segundo = self.pokemon1

        ronda = 1

        while primero.esta_vivo() and segundo.esta_vivo():

            print("\n")
            print("=" * 45)
            print(f"              RONDA {ronda}")
            print("=" * 45)

            # -------------------------
            # Turno del más rápido
            # -------------------------

            self.ejecutar_turno(primero, segundo)

            if not segundo.esta_vivo():

                break

            # -------------------------
            # Respuesta del rival
            # -------------------------

            self.ejecutar_turno(segundo, primero)

            if not primero.esta_vivo():

                break

            ronda += 1

        print("\n")
        print("=" * 45)

        if primero.esta_vivo():

            print(f"🏆 ¡{primero.nombre} es el ganador!")

        else:

            print(f"🏆 ¡{segundo.nombre} es el ganador!")

        print("=" * 45)