# TP TUC Examen

## Groupe
Kouamé BILÉ, Glody KUTUMBAKANA, Joseph HACCANDY

## Contenu realise
- Endpoint de combat entre 2 Pokemons via IDs PokeAPI:
  - `GET /pokemons/battle?first_api_id=<id>&second_api_id=<id>`
  - Compare les stats une a une (`hp`, `attack`, `defense`, `special_attack`, `special_defense`, `speed`).
  - Retourne le gagnant et le score de manches gagnees.
- Endpoint de 3 Pokemons aleatoires avec stats:
  - `GET /pokemons/random`
- Suite de tests unitaires (>= 7) dont tests avec mocks (>= 5).
- Configuration Locust:
  - `locustfile.py`
  - `.locust.conf`

## Lancer l'API
```bash
uvicorn main:app --reload
```

## Lancer les tests unitaires
```bash
pytest -q
```

## Mesurer la couverture
```bash
coverage run -m pytest
coverage report -m
```

## Lancer le test de charge (Locust)
1. Lancer l'API:
```bash
uvicorn main:app --reload
```
2. Dans un autre terminal:
```bash
locust
```
Ou en headless:
```bash
locust --headless -f locustfile.py --host=http://127.0.0.1:8000 -u 20 -r 5 --run-time 1m
```
