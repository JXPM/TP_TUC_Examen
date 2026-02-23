import requests

base_url = "https://pokeapi.co/api/v2"


def get_pokemon_name(api_id):
    """
        Get a pokemon name from the API pokeapi
    """
    return get_pokemon_data(api_id)['name']

def get_pokemon_stats(api_id):
    """
        Get pokemon stats from the API pokeapi
    """
    pokemon_data = get_pokemon_data(api_id)
    stats = {
        "hp": 0,
        "attack": 0,
        "defense": 0,
        "special_attack": 0,
        "special_defense": 0,
        "speed": 0,
    }
    stat_name_mapping = {
        "hp": "hp",
        "attack": "attack",
        "defense": "defense",
        "special-attack": "special_attack",
        "special-defense": "special_defense",
        "speed": "speed",
    }
    for stat in pokemon_data.get("stats", []):
        stat_name = stat.get("stat", {}).get("name")
        normalized_name = stat_name_mapping.get(stat_name)
        if normalized_name is not None:
            stats[normalized_name] = stat.get("base_stat", 0)
    return stats

def get_pokemon_data(api_id):
    """
        Get data of pokemon name from the API pokeapi
    """
    return requests.get(f"{base_url}/pokemon/{api_id}", timeout=10).json()


def battle_pokemon(first_api_id, second_api_id):
    """
        Do battle between 2 pokemons
    """
    first_pokemon_data = get_pokemon_data(first_api_id)
    second_pokemon_data = get_pokemon_data(second_api_id)
    first_stats = get_pokemon_stats(first_api_id)
    second_stats = get_pokemon_stats(second_api_id)
    battle_result = battle_compare_stats(first_stats, second_stats)

    if battle_result > 0:
        winner = first_pokemon_data["name"]
    elif battle_result < 0:
        winner = second_pokemon_data["name"]
    else:
        winner = None

    return {
        "first_pokemon_id": first_api_id,
        "second_pokemon_id": second_api_id,
        "winner": winner,
        "score": {
            "first": sum(
                1 for stat_name in first_stats
                if first_stats[stat_name] > second_stats[stat_name]
            ),
            "second": sum(
                1 for stat_name in second_stats
                if second_stats[stat_name] > first_stats[stat_name]
            ),
        },
    }


def battle_compare_stats(first_pokemon_stats, second_pokemon_stats):
    """
        Compare given stat between two pokemons
    """
    first_wins = 0
    second_wins = 0
    for stat_name, first_value in first_pokemon_stats.items():
        second_value = second_pokemon_stats.get(stat_name, 0)
        if first_value > second_value:
            first_wins += 1
        elif first_value < second_value:
            second_wins += 1

    if first_wins > second_wins:
        return 1
    if second_wins > first_wins:
        return -1
    return 0
