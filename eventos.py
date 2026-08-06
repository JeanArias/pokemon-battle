import random

def aplicar_evento(atacante,defensor):

    evento = random.randint(1,4)
    pokemon = random.choice([atacante,defensor])

    if evento == 1:
        print("\n Evento: Encontro una baya")
        pokemon.curar(20)
        return False

    elif evento ==2:
        print("\n Evento: Ataque critico")
        return "critico"

    elif evento == 3:
        print(f"\n Evento: El {pokemon.nombre} se quedo dormido")
        return "dormido"

    else: 
        print(f"\n Evento: El {pokemon.nombre} ha fallado")
        return "fallado"
        
        


