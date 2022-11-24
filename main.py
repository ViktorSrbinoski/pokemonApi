import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import pokeapi_client
from pokemon import PokemonApiResponse

pokemon_app = FastAPI()

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
    result = pokeapi_client.get_pokemon_list()
    return PokemonApiResponse(result)


@pokemon_app.get("/pokemon/{name}")
def get_specific_pokemon(name):
    return pokeapi_client.get_pokemon_info(name)


@pokemon_app.get("/moves")
def get_request():
    result = pokeapi_client.get_all_damaging_moves()
    return PokemonApiResponse(result)


@pokemon_app.get("/moves/{move}")
def get_move_info(move):
    return pokeapi_client.get_move_info(move)


@pokemon_app.get("/damage/{defender}/{attacker}/{move}")
def pokemon_battle(defender, attacker, move):
    defender = pokeapi_client.get_pokemon_info(defender)
    attacker = pokeapi_client.get_pokemon_info(attacker)
    full_move = pokeapi_client.get_move_info(move)
    return defender.calculate_damage_taken(attacker, full_move)


if __name__ == "__main__":
    uvicorn.run("main:pokemon_app", port=9990, log_level="info")
