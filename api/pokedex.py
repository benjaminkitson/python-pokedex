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

    @property
    def pokemons(self):
        return self._pokemons

    @staticmethod
    def find_pokemon_by_id(pokemons: List[Pokemon], p_id: str):
        for pokemon in pokemons:
            if (pokemon["id"].lower() == p_id):
                return [pokemon]
        return None

    @staticmethod
    def find_pokemon_by_name(pokemons: List[Pokemon], name: str):
        for pokemon in pokemons:
            if (pokemon["name"].lower() == name):
                return [pokemon]
        return None
