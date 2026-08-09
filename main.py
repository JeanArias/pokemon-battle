from pokemons.pikachu import Pikachu
from pokemons.charmander import Charmander
from pokemons.lucario import Lucario

from batalla import Batalla

pikachu = Pikachu()
lucario = Lucario()

batalla = Batalla(pikachu, lucario)

batalla.combatir()
