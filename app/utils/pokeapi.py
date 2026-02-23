"""Utility functions to interact with the PokeAPI."""
import requests

BASE_URL = "https://pokeapi.co/api/v2"


def get_pokemon_name(api_id):
    """Get a pokemon name from the API pokeapi."""
    return get_pokemon_data(api_id)['name']


def get_pokemon_data(api_id):
    """Get data of pokemon from the API pokeapi."""
    return requests.get(f"{BASE_URL}/pokemon/{api_id}", timeout=10).json()


def get_pokemon_stats(api_id):
    """
    Get pokemon stats from the PokeAPI.

    Returns a dict with stat names as keys and base_stat values.
    """
    data = get_pokemon_data(api_id)
    return {s['stat']['name']: s['base_stat'] for s in data['stats']}


def battle_compare_stats(first_pokemon_stats, second_pokemon_stats):
    """
    Compare stats between two pokemons stat by stat.

    Returns a positive integer if first wins, negative if second wins,
    0 if draw.
    """
    score = 0
    all_stats = set(first_pokemon_stats.keys()) | set(second_pokemon_stats.keys())
    for stat in all_stats:
        first_val = first_pokemon_stats.get(stat, 0)
        second_val = second_pokemon_stats.get(stat, 0)
        if first_val > second_val:
            score += 1
        elif second_val > first_val:
            score -= 1
    return score


def battle_pokemon(first_api_id, second_api_id):
    """
    Do battle between 2 pokemons using their PokeAPI IDs.

    Compares each stat one by one. The pokemon with more superior stats wins.
    Returns the winner data or a draw dict.
    """
    first_pokemon = get_pokemon_data(first_api_id)
    second_pokemon = get_pokemon_data(second_api_id)

    first_stats = {s['stat']['name']: s['base_stat'] for s in first_pokemon['stats']}
    second_stats = {s['stat']['name']: s['base_stat'] for s in second_pokemon['stats']}

    battle_result = battle_compare_stats(first_stats, second_stats)

    if battle_result > 0:
        return {'winner': first_pokemon['name'], 'pokemon': first_pokemon}
    if battle_result < 0:
        return {'winner': second_pokemon['name'], 'pokemon': second_pokemon}
    return {'winner': 'draw'}
