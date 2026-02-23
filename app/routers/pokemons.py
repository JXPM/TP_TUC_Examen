"""Router for pokemon endpoints."""
import random
from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from app import actions, schemas
from app.utils.utils import get_db
from app.utils import pokeapi

router = APIRouter()


@router.get("/", response_model=List[schemas.Pokemon])
def get_pokemons(skip: int = 0, limit: int = 100, database: Session = Depends(get_db)):
    """
    Return all pokemons.

    Default limit is 100.
    """
    pokemons = actions.get_pokemons(database, skip=skip, limit=limit)
    return pokemons


@router.get("/battle/{pokemon1_id}/{pokemon2_id}")
def battle_pokemons(pokemon1_id: int, pokemon2_id: int, database: Session = Depends(get_db)):
    """
    Make two pokemons battle using their database IDs.

    Compares each stat one by one. The pokemon with the most superior stats wins.
    """
    pokemon1 = actions.get_pokemon(database, pokemon_id=pokemon1_id)
    if pokemon1 is None:
        raise HTTPException(status_code=404, detail=f"Pokemon {pokemon1_id} not found")

    pokemon2 = actions.get_pokemon(database, pokemon_id=pokemon2_id)
    if pokemon2 is None:
        raise HTTPException(status_code=404, detail=f"Pokemon {pokemon2_id} not found")

    result = pokeapi.battle_pokemon(pokemon1.api_id, pokemon2.api_id)
    return {
        "pokemon1": {"id": pokemon1.id, "name": pokemon1.name, "api_id": pokemon1.api_id},
        "pokemon2": {"id": pokemon2.id, "name": pokemon2.name, "api_id": pokemon2.api_id},
        "result": result
    }


@router.get("/random")
def get_random_pokemons(database: Session = Depends(get_db)):
    """
    Return 3 random pokemons with their stats from PokeAPI.
    """
    all_pokemons = actions.get_pokemons(database)
    if len(all_pokemons) < 3:
        raise HTTPException(
            status_code=404,
            detail="Not enough pokemons in database (need at least 3)"
        )

    selected = random.sample(all_pokemons, 3)
    result = []
    for poke in selected:
        stats = pokeapi.get_pokemon_stats(poke.api_id)
        result.append({
            "id": poke.id,
            "name": poke.name,
            "api_id": poke.api_id,
            "custom_name": poke.custom_name,
            "trainer_id": poke.trainer_id,
            "stats": stats
        })
    return result
