from locust import HttpUser, between, task


class PokemonApiUser(HttpUser):
    wait_time = between(1, 2)

    @task(3)
    def list_pokemons(self):
        self.client.get("/pokemons/")

    @task(2)
    def pokemon_battle(self):
        self.client.get("/pokemons/battle", params={"first_api_id": 1, "second_api_id": 4})

    @task(1)
    def random_pokemons(self):
        self.client.get("/pokemons/random")
