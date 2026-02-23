from datetime import date
from typing import Dict, List, Optional, Union
from pydantic import BaseModel

#
#  ITEM
#
class ItemBase(BaseModel):
    name: str
    description: Union[str, None] = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    trainer_id: int

    class Config:
        orm_mode = True

#
#  POKEMON
#
class PokemonBase(BaseModel):
    api_id: int
    custom_name: Optional[str] = None

class PokemonCreate(PokemonBase):
    pass

class Pokemon(PokemonBase):
    id: int
    name: str
    trainer_id: int

    class Config:
        orm_mode = True


class PokemonStats(BaseModel):
    hp: int
    attack: int
    defense: int
    special_attack: int
    special_defense: int
    speed: int


class PokemonBattleResult(BaseModel):
    first_pokemon_id: int
    second_pokemon_id: int
    winner: Union[str, None]
    score: Dict[str, int]


class PokemonWithStats(BaseModel):
    api_id: int
    name: str
    stats: PokemonStats
#
#  TRAINER
#
class TrainerBase(BaseModel):
    name: str
    birthdate: date

class TrainerCreate(TrainerBase):
    pass

class Trainer(TrainerBase):
    id: int
    inventory: List[Item] = []
    pokemons: List[Pokemon] = []

    class Config:
        orm_mode = True
