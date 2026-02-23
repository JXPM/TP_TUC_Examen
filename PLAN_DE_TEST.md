# Plan de test - TP TUC Examen

## 1. Informations generales
- Projet: API FastAPI de gestion de dresseurs/pokemons/items
- Version cible: etat courant du repository
- Date: 23/02/2026
- Auteur: a completer
- Groupe: a completer (3 ou 4)

## 2. Objectifs
- Verifier la conformite fonctionnelle des endpoints.
- Verifier la logique de combat Pokemon demandee a l'examen.
- Verifier la robustesse minimale (erreurs API externe, statuts HTTP).
- Verifier la tenue en charge de base avec Locust.
- Atteindre les attendus examen:
  - Tests unitaires: >= 7 (groupe 4) / >= 5 (groupe 3)
  - Tests avec mocks: >= 5 (groupe 4) / >= 3 (groupe 3)
  - Coverage: >= 85% (groupe 4) / >= 80% (groupe 3)

## 3. Perimetre
- Inclus:
  - `GET /pokemons/battle`
  - `GET /pokemons/random`
  - Endpoints existants trainers/items/pokemons
  - Fonctions metier de `app/utils/pokeapi.py`
  - Fonctions CRUD de `app/actions.py`
- Hors perimetre:
  - Tests UI (pas d'interface front)
  - Tests securite avances (pentest, auth, OWASP complet)

## 4. Environnement de test
- OS: Linux
- Python: 3.10.x
- Framework API: FastAPI
- Base de donnees: SQLite (`sqlite.db`)
- Outils:
  - `pytest`
  - `coverage`
  - `locust`
  - `pylint`

## 5. Strategie de test
- Niveau 1: Unitaires purs (fonctions de comparaison et regles combat)
- Niveau 2: Unitaires avec mocks (PokeAPI/DB) pour isoler la logique
- Niveau 3: Tests API (endpoints battle/random, statuts et structure payload)
- Niveau 4: Performance de base avec Locust (charge legere)
- Niveau 5: Qualite statique avec pylint

## 6. Donnees de test
- IDs Pokemon valides: 1, 4, 7
- Cas de stats fabriquees (mocks):
  - Cas victoire premier pokemon
  - Cas victoire second pokemon
  - Cas egalite
- Cas API externe indisponible: simulation via mock d'exception HTTP

## 7. Matrice de tracabilite exigences -> tests
| Exigence | Description | Tests associes |
|---|---|---|
| EX-01 | Combat entre 2 Pokemons par IDs | `test_battle_pokemon_first_wins`, `test_battle_pokemon_draw`, `test_pokemon_battle_endpoint` |
| EX-02 | Comparaison stats 1 a 1 | `test_battle_compare_stats_first_wins`, `test_battle_compare_stats_second_wins`, `test_battle_compare_stats_draw` |
| EX-03 | Endpoint 3 Pokemons aleatoires + stats (groupe 4) | `test_random_pokemons_endpoint` |
| EX-04 | Ajout Pokemon a un trainer + nom issu PokeAPI | `test_add_trainer_pokemon_uses_pokeapi_name` |
| EX-05 | Creation trainer + transactions DB | `test_create_trainer_creates_and_commits` |
| EX-06 | Mapping des stats PokeAPI vers schema interne | `test_get_pokemon_stats_maps_api_stats` |

## 8. Cas de test detailles
| ID | Type | Description | Pre-conditions | Etapes | Resultat attendu |
|---|---|---|---|---|---|
| TU-01 | Unitaire | `battle_compare_stats` retourne 1 | Stats mockees | Comparer 2 dicts (premier meilleur) | Retour `1` |
| TU-02 | Unitaire | `battle_compare_stats` retourne -1 | Stats mockees | Comparer 2 dicts (second meilleur) | Retour `-1` |
| TU-03 | Unitaire | `battle_compare_stats` retourne 0 | Stats mockees | Comparer 2 dicts (egalite) | Retour `0` |
| TU-04 | Unitaire+mock | Mapping stats PokeAPI | Mock `get_pokemon_data` | Appeler `get_pokemon_stats(1)` | Dict normalise correct |
| TU-05 | Unitaire+mock | Combat: victoire premier | Mock PokeAPI | Appeler `battle_pokemon(1,4)` | `winner` = premier, score coherent |
| TU-06 | Unitaire+mock | Combat: egalite | Mock PokeAPI | Appeler `battle_pokemon(1,4)` | `winner` = `None`, score nul |
| TA-01 | API+mock | Endpoint `/pokemons/battle` | Router charge | Appel route avec 2 IDs | JSON conforme + gagnant attendu |
| TA-02 | API+mock | Endpoint `/pokemons/random` | Router charge | Appel route random | 3 elements, stats presentes |
| TC-01 | CRUD+mock | Ajout pokemon trainer | Mock DB + models | Appeler `add_trainer_pokemon` | `add/commit/refresh` appeles |
| TC-02 | CRUD+mock | Creation trainer | Mock DB + models | Appeler `create_trainer` | `add/commit/refresh` appeles |

## 9. Execution automatique
- Lancer les tests:
```bash
pytest -q
```
- Mesurer la couverture:
```bash
test__venv/bin/coverage run -m pytest -q
test__venv/bin/coverage report -m
```
- Verifier la qualite statique:
```bash
PYLINTHOME=/tmp/pylint_home test__venv/bin/pylint --rcfile=.pylintrc app main.py
```

## 10. Resultats constates (etat actuel)
- Tests unitaires: 10/10 passes
- Nombre de tests avec mocks: 7+
- Coverage total observe: 91%
- Pylint observe: 10.00/10 (avec `.pylintrc` du projet)

## 11. Plan de charge (Locust)
### 11.1 Objectif
- Evaluer un comportement de base sous charge legere sur:
  - `GET /pokemons/`
  - `GET /pokemons/battle`
  - `GET /pokemons/random`

### 11.2 Configuration
- Fichier: `locustfile.py`
- Host par defaut: `http://127.0.0.1:8000`
- Taches:
  - liste pokemons: poids 3
  - battle: poids 2
  - random: poids 1

### 11.3 Procedure
1. Demarrer l'API:
```bash
uvicorn main:app --reload
```
2. Demarrer Locust UI:
```bash
locust -f locustfile.py
```
3. Ouvrir `http://127.0.0.1:8089`
4. Lancer un scenario type: 20 users, spawn rate 5, duree 1 min

### 11.4 Criteres d'acceptation charge (cible de base)
- Taux d'erreur < 5%
- p95 < 1000 ms sur endpoints principaux
- Pas de crash applicatif

## 12. Risques et mitigations
| Risque | Impact | Mitigation |
|---|---|---|
| Indisponibilite ou rate-limit PokeAPI | Stats manquantes, erreurs battle/random | Mock en tests + gestion d'erreur HTTP cote API |
| Ecart de perf selon machine locale | Resultats charge variables | Standardiser scenario (users, duree, host) |
| Regressions lors de modifications futures | Defauts non detectes | Rejouer `pytest`, `coverage`, `pylint` en CI |

## 13. Critere Go/No-Go
- Go si:
  - Tous les tests passent
  - Coverage >= seuil groupe
  - Pylint >= seuil groupe
  - Endpoint combat et random verifies
- No-Go sinon

## 14. Annexes
- Tests: `tests/test_pokeapi.py`, `tests/test_routes_and_actions.py`
- Charge: `locustfile.py`, `locust.conf`
- Documentation: `README.md`
