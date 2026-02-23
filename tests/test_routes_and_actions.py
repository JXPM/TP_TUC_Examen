from unittest.mock import Mock, patch

from app import actions, schemas
from app.routers import pokemons as pokemons_router


def test_pokemon_battle_endpoint():
    with patch(
        "app.routers.pokemons.battle_pokemon",
        return_value={
            "first_pokemon_id": 1,
            "second_pokemon_id": 4,
            "winner": "bulbasaur",
            "score": {"first": 4, "second": 2},
        },
    ):
        response = pokemons_router.pokemon_battle(first_api_id=1, second_api_id=4)

    assert response["winner"] == "bulbasaur"


def test_random_pokemons_endpoint():
    with patch("app.routers.pokemons.random.sample", return_value=[1, 4, 7]), patch(
        "app.routers.pokemons.get_pokemon_data",
        side_effect=[{"name": "bulbasaur"}, {"name": "charmander"}, {"name": "squirtle"}],
    ), patch(
        "app.routers.pokemons.get_pokemon_stats",
        side_effect=[
            {
                "hp": 45,
                "attack": 49,
                "defense": 49,
                "special_attack": 65,
                "special_defense": 65,
                "speed": 45,
            },
            {
                "hp": 39,
                "attack": 52,
                "defense": 43,
                "special_attack": 60,
                "special_defense": 50,
                "speed": 65,
            },
            {
                "hp": 44,
                "attack": 48,
                "defense": 65,
                "special_attack": 50,
                "special_defense": 64,
                "speed": 43,
            },
        ],
    ):
        response = pokemons_router.get_random_pokemons()

    assert len(response) == 3
    assert response[0]["name"] == "bulbasaur"
    assert response[1]["stats"]["speed"] == 65


def test_add_trainer_pokemon_uses_pokeapi_name():
    mock_db = Mock()
    mock_db_item = Mock(id=1, api_id=1, name="bulbasaur", custom_name="leafy", trainer_id=10)
    with patch("app.actions.get_pokemon_name", return_value="bulbasaur"), patch(
        "app.models.Pokemon", return_value=mock_db_item
    ):
        created = actions.add_trainer_pokemon(
            mock_db,
            schemas.PokemonCreate(api_id=1, custom_name="leafy"),
            trainer_id=10,
        )

    assert created == mock_db_item
    mock_db.add.assert_called_once_with(mock_db_item)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(mock_db_item)


def test_create_trainer_creates_and_commits():
    mock_db = Mock()
    mock_trainer = Mock(id=1, name="Ash")
    with patch("app.models.Trainer", return_value=mock_trainer):
        created = actions.create_trainer(
            mock_db,
            schemas.TrainerCreate(name="Ash", birthdate="2000-01-01"),
        )

    assert created == mock_trainer
    mock_db.add.assert_called_once_with(mock_trainer)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(mock_trainer)
