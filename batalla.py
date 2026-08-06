from eventos import aplicar_evento
import time

class Batalla:

    def __init__(self,pokemon1,pokemon2):
        self.pokemon1 = pokemon1
        self.pokemon2 = pokemon2

    def mostrar_estados(self):
        print("\n==========================")
        self.pokemon1.mostrar_estado()
        print("----------------------------")
        self.pokemon2.mostrar_estado()
        print("==========================\n")

    def pausar(self):
        input("\n Presione ENTER para continuar...")

    def ejecutar_turno(self,atacante,defensor):

        print(f"\n Turno de {atacante.nombre}")
        time.sleep(1)
        evento = aplicar_evento(atacante,defensor)

        if evento == "dormido":
            print(f"{atacante.nombre} esta dormido")
            print("Pierde el turno")
            self.pausar()
            return

        #-----------------------
        if evento == "fallado":
                    print(f"{atacante.nombre} fallo el ataque")
        
                    self.pausar()
                    return

        #-----------------------
        daño = atacante.atacar()
        if evento == "critico":
                daño *=2
                print("ATAQUE CRITICO!!!")

        defensor.recibir_daño(daño)
                
        self.pausar()
        self.mostrar_estados()
        self.pausar()

        #-----------------------

    def combatir(self):

        print("="*40)
        print("         BATALLA POKEMON")
        print("="*40)

        self.mostrar_estados()
        self.pausar()

        if self.pokemon1.velocidad >= self.pokemon2.velocidad:
            primero = self.pokemon1
            segundo = self.pokemon2
           
        else:
            primero = self.pokemon2
            segundo = self.pokemon1
           

        ronda = 1

        while primero.esta_vivo() and segundo.esta_vivo():

            print("="*40)
            print(f"        RONDA {ronda}")
            print("="*40)

            self.ejecutar_turno(primero,segundo)

            if not segundo.esta_vivo() :
                break

            self.ejecutar_turno(segundo,primero)

            if not primero.esta_vivo() :
                break
            
            ronda += 1

        print("="*40)
        if primero.esta_vivo():
             print(f"{primero.nombre} es el ganador")

        else:
            print(f"{segundo.nombre} es el ganador")
        print("="*40)




        

        

