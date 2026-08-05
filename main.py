from pokemons.pikachu import Pikachu
from pokemons.charmander import Charmander
from batalla import Batalla


pikachu = Pikachu()

charmander = Charmander()

batalla = Batalla(
    pikachu,
    charmander
)

batalla.combatir()