from locust import HttpUser, between, task


class PokemonApiUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def list_pokemons(self):
        self.client.get("/pokemons/")

    @task(2)
    def pokemon_battle(self):
        self.client.get("/pokemons/battle", params={"first_api_id": 1, "second_api_id": 4})

    @task(1)
    def random_pokemons(self):
        self.client.get("/pokemons/random")
        

    @task(3)
    def list_trainers(self):
        """List all trainers."""
        self.client.get("/trainers/")

    @task(2)
    def list_items(self):
        """List all items."""
        self.client.get("/items/")

    @task(1)
    def battle_pokemons(self):
        """Battle two pokemons."""
        self.client.get("/pokemons/battle/1/2")

    @task(1)
    def get_trainer_by_id(self):
        """Get a specific trainer."""
        self.client.get("/trainers/1")
