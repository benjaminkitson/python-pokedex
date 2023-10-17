import json
from pokedex import Pokedex
import pytest

with open('api/test-pokemon.json') as file:
    data = json.load(file)


def test_id_filter():
    pokedex = Pokedex(data["pokemon"])

    pokedex.apply_filter("id", "1")

    filtered_pokemon = pokedex.get_filtered_pokemon()

    print(filtered_pokemon)

    assert filtered_pokemon[0]["id"] == "1"


def test_name_filter():
    pokedex = Pokedex(data["pokemon"])

    pokedex.apply_filter("name", "charmander")

    filtered_pokemon = pokedex.get_filtered_pokemon()

    assert filtered_pokemon[0]["name"] == "Charmander"


def test_multiple_filters():
    pokedex = Pokedex(data["pokemon"])

    pokedex.apply_filter("name", "charmander")
    pokedex.apply_filter("id", "4")

    filtered_pokemon = pokedex.get_filtered_pokemon()

    assert filtered_pokemon[0]["id"] == "4"


def test_incompatible_filters():
    pokedex = Pokedex(data["pokemon"])

    pokedex.apply_filter("name", "charmander")
    pokedex.apply_filter("id", "3")

    filtered_pokemon = pokedex.get_filtered_pokemon()

    assert len(filtered_pokemon) == 0


def test_invalid_filter():
    pokedex = Pokedex(data["pokemon"])

    with pytest.raises(KeyError):
        pokedex.apply_filter("invalid", "charmander")
