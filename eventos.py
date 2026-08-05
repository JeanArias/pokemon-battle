import random


def aplicar_evento(atacante, defensor):

    evento = random.randint(1, 4)

    if evento == 1:

        print("\n🍓 Evento: Encontró una baya.")

        atacante.curar(20)

        return False

    elif evento == 2:

        print("\n💥 Evento: Ataque crítico.")

        return "critico"

    elif evento == 3:

        print("\n😴 Evento: El atacante se quedó dormido.")

        return "dormido"

    else:

        print("\n🛡 Evento: El defensor esquivó el ataque.")

        return "esquivar"