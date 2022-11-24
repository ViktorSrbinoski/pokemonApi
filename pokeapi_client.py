import requests
from pokemon import Overview
from pokemon import Pokemon
from pokemon import BaseStats
from pokemon import Move


def get_pokemon_list():
    pokemon_dict = {}
    response = requests.get("https://pokeapi.co/api/v2/pokemon?offset=0&limit=2000")
    for result in response.json()["results"]:
        pokemon_dict[result["name"]] = result["url"]
    return pokemon_dict


def get_pokemon_info(url):
    response = requests.get(url).json()
    base_stats = BaseStats(response["stats"][0]["base_stat"], response["stats"][1]["base_stat"],
                           response["stats"][2]["base_stat"], response["stats"][3]["base_stat"],
                           response["stats"][4]["base_stat"], response["stats"][5]["base_stat"])
    type1 = response["types"][0]["type"]["name"]
    type2 = None
    if len(response["types"]) == 2:
        type2 = response["types"][1]["type"]["name"]
    pokemon = Pokemon(response["name"], base_stats, 50, type1, type2, response["sprites"]["front_default"])
    return pokemon


def get_all_damaging_moves():
    damage_categories = ["0", "4", "6", "7"]
    all_moves = {}
    for category in damage_categories:
        response = requests.get("https://pokeapi.co/api/v2/move-category/" + category).json()
        for move in response["moves"]:
            all_moves[move["name"]] = move["url"]
    return all_moves


def get_move_info(move):
    response = requests.get("https://pokeapi.co/api/v2/move/" + move).json()
    if response["damage_class"]["name"] == "physical":
        is_physical = True
    else:
        is_physical = False
    return Move(response["name"], response["type"]["name"], is_physical, response["power"], response["accuracy"], response["priority"])
