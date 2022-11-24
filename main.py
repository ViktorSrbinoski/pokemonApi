import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pokeapi_client
from pokemon import PokemonApiResponse

pokemon_app = FastAPI()
all_pokemon = dict()
all_moves = dict()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

pokemon_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@pokemon_app.get("/pokemon")
def get_all_pokemon():
    global all_pokemon
    all_pokemon = pokeapi_client.get_pokemon_list()
    result = []
    for name in all_pokemon:
        result.append(pokeapi_client.Overview(name, all_pokemon[name]))
    return PokemonApiResponse(result)


@pokemon_app.get("/pokemon/{name}")
def get_specific_pokemon(name):
    global all_pokemon
    return pokeapi_client.get_pokemon_info(all_pokemon[name])


@pokemon_app.get("/moves")
def get_request():
    global all_moves
    all_moves = pokeapi_client.get_all_damaging_moves()
    result = []
    for move in all_moves:
        result.append(pokeapi_client.Overview(move, all_moves[move]))
    return PokemonApiResponse(result)


@pokemon_app.get("/moves/{move}")
def get_move_info(move):
    return pokeapi_client.get_move_info(move)


@pokemon_app.get("/damage/{defender}/{attacker}/{move}")
def pokemon_battle(defender, attacker, move):
    defender = pokeapi_client.get_pokemon_info(all_pokemon[defender])
    attacker = pokeapi_client.get_pokemon_info(all_pokemon[attacker])
    full_move = pokeapi_client.get_move_info(move)
    return defender.calculate_damage_taken(attacker, full_move)


if __name__ == "__main__":
    uvicorn.run("main:pokemon_app", port=9990, log_level="info")
