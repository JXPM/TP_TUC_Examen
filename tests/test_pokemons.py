import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from app.utils.pokeapi import battle_compare_stats, battle_pokemon, get_pokemon_stats
from main import app

client = TestClient(app)

# Données de test

BULBASAUR_STATS = {
    "hp": 45, "attack": 49, "defense": 49,
    "special-attack": 65, "special-defense": 65, "speed": 45
}
CHARMANDER_STATS = {
    "hp": 39, "attack": 52, "defense": 43,
    "special-attack": 60, "special-defense": 50, "speed": 65
}
MEWTWO_STATS = {
    "hp": 106, "attack": 110, "defense": 90,
    "special-attack": 154, "special-defense": 90, "speed": 130
}


def make_api_payload(name, stats_dict):
    """Construit un payload PokeAPI minimal."""
    return {
        "name": name,
        "id": 1,
        "stats": [{"stat": {"name": k}, "base_stat": v} for k, v in stats_dict.items()]
    }


#  Tests unitaires 

class TestBattleCompareStats(unittest.TestCase):
    """Tests sur la logique de comparaison de stats."""

    def test_first_wins_when_more_superior_stats(self):
        """Le 1er gagne quand toutes ses stats sont supérieures."""
        first = {"hp": 100, "attack": 100, "defense": 100}
        second = {"hp": 10, "attack": 10, "defense": 10}
        self.assertGreater(battle_compare_stats(first, second), 0)

    def test_second_wins_when_more_superior_stats(self):
        """Le 2e gagne quand toutes ses stats sont supérieures."""
        first = {"hp": 10, "attack": 10, "defense": 10}
        second = {"hp": 100, "attack": 100, "defense": 100}
        self.assertLess(battle_compare_stats(first, second), 0)

    def test_draw_when_equal_stats(self):
        """Retourne 0 quand toutes les stats sont égales."""
        stats = {"hp": 50, "attack": 50, "defense": 50}
        self.assertEqual(battle_compare_stats(stats, stats.copy()), 0)

    def test_mixed_stats_count_wins_correctly(self):
        """Compte correctement les victoires par stat."""
        # 1 victoire pour first, 2 pour second → négatif
        first = {"hp": 100, "attack": 10, "defense": 10}
        second = {"hp": 10, "attack": 100, "defense": 100}
        self.assertLess(battle_compare_stats(first, second), 0)

    def test_empty_stats_returns_draw(self):
        """Deux dicts vides → égalité."""
        self.assertEqual(battle_compare_stats({}, {}), 0)

    def test_missing_stat_treated_as_zero(self):
        """Une stat absente est comptée comme 0."""
        first = {"hp": 1}
        second = {}
        self.assertGreater(battle_compare_stats(first, second), 0)

    def test_bulbasaur_beats_charmander(self):
        """Bulbasaur gagne contre Charmander (4 stats > 2 stats)."""
        result = battle_compare_stats(BULBASAUR_STATS, CHARMANDER_STATS)
        self.assertGreater(result, 0)


# Tests avec Mocks
class TestBattlePokemonMocked(unittest.TestCase):
    """Tests de battle_pokemon avec HTTP mocké."""

    @patch('app.utils.pokeapi.requests.get')
    def test_battle_pokemon_first_wins(self, mock_get):
        """battle_pokemon retourne le 1er quand il domine les stats."""
        mewtwo_payload = make_api_payload("mewtwo", MEWTWO_STATS)
        bulbasaur_payload = make_api_payload("bulbasaur", BULBASAUR_STATS)
        mock_get.side_effect = [
            MagicMock(json=lambda: mewtwo_payload),
            MagicMock(json=lambda: bulbasaur_payload),
        ]
        result = battle_pokemon(150, 1)
        self.assertEqual(result['winner'], 'mewtwo')

    @patch('app.utils.pokeapi.requests.get')
    def test_battle_pokemon_draw(self, mock_get):
        """battle_pokemon retourne draw quand les stats sont identiques."""
        same = {"hp": 50, "attack": 50, "defense": 50,
                "special-attack": 50, "special-defense": 50, "speed": 50}
        payload = make_api_payload("cloneA", same)
        mock_get.side_effect = [
            MagicMock(json=lambda: payload),
            MagicMock(json=lambda: make_api_payload("cloneB", same)),
        ]
        result = battle_pokemon(1, 2)
        self.assertEqual(result['winner'], 'draw')

    @patch('app.utils.pokeapi.requests.get')
    def test_battle_pokemon_second_wins(self, mock_get):
        """battle_pokemon retourne le 2e quand il domine les stats."""
        bulbasaur_payload = make_api_payload("bulbasaur", BULBASAUR_STATS)
        mewtwo_payload = make_api_payload("mewtwo", MEWTWO_STATS)
        mock_get.side_effect = [
            MagicMock(json=lambda: bulbasaur_payload),
            MagicMock(json=lambda: mewtwo_payload),
        ]
        result = battle_pokemon(1, 150)
        self.assertEqual(result['winner'], 'mewtwo')

    @patch('app.utils.pokeapi.requests.get')
    def test_get_pokemon_stats_returns_dict(self, mock_get):
        """get_pokemon_stats parse correctement le payload PokeAPI."""
        mock_get.return_value = MagicMock(
            json=lambda: make_api_payload("bulbasaur", BULBASAUR_STATS)
        )
        result = get_pokemon_stats(1)
        self.assertIsInstance(result, dict)
        self.assertEqual(result['hp'], 45)
        self.assertEqual(result['attack'], 49)

    def test_battle_endpoint_404_unknown_pokemon(self):
        """L'endpoint /battle/ retourne 404 si le pokemon n'existe pas en BDD."""
        response = client.get("/pokemons/battle/99999/99998")
        self.assertEqual(response.status_code, 404)


# ─── Tests des endpoints REST ─────────────────────────────────────────────────

class TestPokemonsEndpoints(unittest.TestCase):
    """Tests d'intégration des endpoints Pokemon."""

    def test_get_pokemons_returns_list(self):
        """GET /pokemons/ retourne une liste."""
        response = client.get("/pokemons/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_battle_invalid_ids_returns_404(self):
        """GET /pokemons/battle/ avec des IDs inexistants → 404."""
        response = client.get("/pokemons/battle/99999/99998")
        self.assertEqual(response.status_code, 404)


class TestActionsAndRouters(unittest.TestCase):
    """Tests complémentaires pour la couverture."""

    def test_get_trainers_returns_list(self):
        """GET /trainers retourne une liste."""
        response = client.get("/trainers")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_get_trainer_not_found(self):
        """GET /trainers/{id} → 404 pour un ID inconnu."""
        response = client.get("/trainers/99999")
        self.assertEqual(response.status_code, 404)

    def test_get_items_returns_list(self):
        """GET /items/ retourne une liste."""
        response = client.get("/items/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_create_trainer(self):
        """POST /trainers/ crée un dresseur."""
        payload = {"name": "AshKetchum", "birthdate": "2000-05-22"}
        response = client.post("/trainers/", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "AshKetchum")

    @patch('app.routers.pokemons.pokeapi.get_pokemon_stats')
    @patch('app.routers.pokemons.actions.get_pokemons')
    def test_random_pokemons_returns_3(self, mock_get_pokemons, mock_stats):
        """GET /pokemons/random retourne 3 pokemons avec leurs stats."""
        mock_poke = MagicMock()
        mock_poke.id = 1
        mock_poke.name = "bulbasaur"
        mock_poke.api_id = 1
        mock_poke.custom_name = None
        mock_poke.trainer_id = 1
        mock_get_pokemons.return_value = [mock_poke, mock_poke, mock_poke]
        mock_stats.return_value = BULBASAUR_STATS

        response = client.get("/pokemons/random")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)

    @patch('app.routers.pokemons.actions.get_pokemons')
    def test_random_pokemons_not_enough(self, mock_get_pokemons):
        """GET /pokemons/random → 404 si moins de 3 pokemons en BDD."""
        mock_get_pokemons.return_value = []
        response = client.get("/pokemons/random")
        self.assertEqual(response.status_code, 404)

    def test_age_from_birthdate(self):
        """age_from_birthdate retourne le bon âge."""
        from datetime import date
        from app.utils.utils import age_from_birthdate
        age = age_from_birthdate(date(2000, 1, 1))
        self.assertGreaterEqual(age, 25)


if __name__ == "__main__":
    unittest.main()
