from app.utils import pokeapi
from unittest.mock import patch


def test_battle_compare_stats_first_wins():
    first = {
        "hp": 100,
        "attack": 100,
        "defense": 50,
        "special_attack": 50,
        "special_defense": 50,
        "speed": 50,
    }
    second = {
        "hp": 90,
        "attack": 90,
        "defense": 40,
        "special_attack": 40,
        "special_defense": 40,
        "speed": 40,
    }

    assert pokeapi.battle_compare_stats(first, second) == 1


def test_battle_compare_stats_second_wins():
    first = {
        "hp": 50,
        "attack": 50,
        "defense": 50,
        "special_attack": 50,
        "special_defense": 50,
        "speed": 50,
    }
    second = {
        "hp": 80,
        "attack": 80,
        "defense": 80,
        "special_attack": 80,
        "special_defense": 80,
        "speed": 80,
    }

    assert pokeapi.battle_compare_stats(first, second) == -1


def test_battle_compare_stats_draw():
    first = {
        "hp": 100,
        "attack": 50,
        "defense": 40,
        "special_attack": 20,
        "special_defense": 20,
        "speed": 30,
    }
    second = {
        "hp": 50,
        "attack": 100,
        "defense": 80,
        "special_attack": 20,
        "special_defense": 20,
        "speed": 10,
    }

    assert pokeapi.battle_compare_stats(first, second) == 0


def test_get_pokemon_stats_maps_api_stats():
    with patch(
        "app.utils.pokeapi.get_pokemon_data",
        return_value={
            "stats": [
                {"base_stat": 45, "stat": {"name": "hp"}},
                {"base_stat": 49, "stat": {"name": "attack"}},
                {"base_stat": 49, "stat": {"name": "defense"}},
                {"base_stat": 65, "stat": {"name": "special-attack"}},
                {"base_stat": 65, "stat": {"name": "special-defense"}},
                {"base_stat": 45, "stat": {"name": "speed"}},
            ]
        },
    ):
        stats = pokeapi.get_pokemon_stats(1)

    assert stats == {
        "hp": 45,
        "attack": 49,
        "defense": 49,
        "special_attack": 65,
        "special_defense": 65,
        "speed": 45,
    }


def test_battle_pokemon_first_wins():
    with patch(
        "app.utils.pokeapi.get_pokemon_data",
        side_effect=[{"name": "bulbasaur"}, {"name": "charmander"}],
    ), patch(
        "app.utils.pokeapi.get_pokemon_stats",
        side_effect=[
            {
                "hp": 90,
                "attack": 90,
                "defense": 90,
                "special_attack": 90,
                "special_defense": 90,
                "speed": 90,
            },
            {
                "hp": 10,
                "attack": 10,
                "defense": 10,
                "special_attack": 10,
                "special_defense": 10,
                "speed": 10,
            },
        ],
    ):
        result = pokeapi.battle_pokemon(1, 4)

    assert result["winner"] == "bulbasaur"
    assert result["score"] == {"first": 6, "second": 0}


def test_battle_pokemon_draw():
    with patch(
        "app.utils.pokeapi.get_pokemon_data",
        side_effect=[{"name": "bulbasaur"}, {"name": "charmander"}],
    ), patch(
        "app.utils.pokeapi.get_pokemon_stats",
        side_effect=[
            {
                "hp": 50,
                "attack": 50,
                "defense": 50,
                "special_attack": 50,
                "special_defense": 50,
                "speed": 50,
            },
            {
                "hp": 50,
                "attack": 50,
                "defense": 50,
                "special_attack": 50,
                "special_defense": 50,
                "speed": 50,
            },
        ],
    ):
        result = pokeapi.battle_pokemon(1, 4)

    assert result["winner"] is None
    assert result["score"] == {"first": 0, "second": 0}
