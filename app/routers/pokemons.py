import random
from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter,  Depends
from app import actions, schemas
from app.utils.pokeapi import battle_pokemon, get_pokemon_data, get_pokemon_stats
from app.utils.utils import get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.Pokemon])
def get_pokemons(skip: int = 0, limit: int = 100, database: Session = Depends(get_db)):
    """
        Return all pokemons
        Default limit is 100
    """
    pokemons = actions.get_pokemons(database, skip=skip, limit=limit)
    return pokemons


@router.get("/battle", response_model=schemas.PokemonBattleResult)
def pokemon_battle(first_api_id: int, second_api_id: int):
    """
        Do a battle between two pokemons using pokeapi ids
    """
    return battle_pokemon(first_api_id=first_api_id, second_api_id=second_api_id)


@router.get("/random", response_model=List[schemas.PokemonWithStats])
def get_random_pokemons():
    """
        Return 3 random pokemons with stats
    """
    random_ids = random.sample(range(1, 1026), 3)
    random_pokemons = []
    for pokemon_id in random_ids:
        pokemon_data = get_pokemon_data(pokemon_id)
        random_pokemons.append({
            "api_id": pokemon_id,
            "name": pokemon_data["name"],
            "stats": get_pokemon_stats(pokemon_id),
        })
    return random_pokemons
