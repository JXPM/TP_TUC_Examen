"""Locust performance tests for the Pokemon API."""
from locust import HttpUser, task, between


class PokemonAPIUser(HttpUser):
    """Simulates a user interacting with the Pokemon API."""
    wait_time = between(1, 3)

    @task(3)
    def list_pokemons(self):
        """List all pokemons - most frequent action."""
        self.client.get("/pokemons/")

    @task(3)
    def list_trainers(self):
        """List all trainers."""
        self.client.get("/trainers/")

    @task(2)
    def list_items(self):
        """List all items."""
        self.client.get("/items/")

    @task(2)
    def get_random_pokemons(self):
        """Get 3 random pokemons with stats."""
        self.client.get("/pokemons/random")

    @task(1)
    def battle_pokemons(self):
        """Battle two pokemons."""
        self.client.get("/pokemons/battle/1/2")

    @task(1)
    def get_trainer_by_id(self):
        """Get a specific trainer."""
        self.client.get("/trainers/1")
