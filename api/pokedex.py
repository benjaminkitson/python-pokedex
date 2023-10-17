from dataclasses import dataclass
from typing import List


@dataclass
class Pokemon():
    name: str
    ability: str
    description: str
    evolutionChain: List[str]
    height: int
    id: str
    mainImageSrc: str
    thumbImageSrc: str
    types: List[str]
    weight: int


class Pokedex():
    def __init__(self, pokemons: List[Pokemon]):
        self._pokemons = pokemons
        # This could probably be a class of its own
        self._filters = {
            "id": None,
            "name": None,
        }

    @property
    def pokemons(self):
        return self._pokemons

    def apply_filter(self, filter, value):
        self._filters[filter] = value
        print(self._filters)

    def get_filtered_pokemon(self):
        filtered_pokemon = self._pokemons
        filtered_pokemon_container = []
        for filter in self._filters:
            if self._filters[filter] != None:
                for pokemon in filtered_pokemon:
                    if (pokemon[filter].lower() == self._filters[filter]):
                        print(pokemon)
                        filtered_pokemon_container.append(pokemon)
                filtered_pokemon = filtered_pokemon_container[:]
                filtered_pokemon_container = []
        return filtered_pokemon
