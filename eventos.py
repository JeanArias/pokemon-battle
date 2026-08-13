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
        
#esto es nuevoooo
       

def aplicar_evento_detallado(atacante, defensor):
    """Version estructurada para la interfaz grafica.

    Mantiene los cuatro eventos del juego, pero devuelve informacion
    adicional para que la GUI sepa que Pokemon fue afectado.
    """
    evento = random.randint(1, 4)

    if evento == 1:
        objetivo = random.choice([atacante, defensor])
        objetivo.curar(20)
        return {
            "tipo": "baya",
            "objetivo": objetivo,
            "texto": f"{objetivo.nombre} encontro una baya y recupero 20 HP."
        }

    if evento == 2:
        return {
            "tipo": "critico",
            "objetivo": atacante,
            "texto": f"{atacante.nombre} consiguio un ATAQUE CRITICO."
        }

    if evento == 3:
        objetivo = random.choice([atacante, defensor])
        return {
            "tipo": "dormido",
            "objetivo": objetivo,
            "texto": f"{objetivo.nombre} se quedo dormido y perdera su proximo turno."
        }

    return {
        "tipo": "fallado",
        "objetivo": atacante,
        "texto": f"{atacante.nombre} fallo el ataque."
    }



