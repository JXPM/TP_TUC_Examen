# Annexe - Cas de test detailles

## CT-01 - Battle valide
- Priorite: P1
- Type: API fonctionnel
- Pre-conditions: API lancee
- Entree: `GET /pokemons/battle?first_api_id=1&second_api_id=4`
- Resultat attendu:
  - HTTP 200
  - Corps avec `first_pokemon_id`, `second_pokemon_id`, `winner`, `score`
  - `score.first` et `score.second` coherents

## CT-02 - Random valide
- Priorite: P1
- Type: API fonctionnel
- Pre-conditions: API lancee
- Entree: `GET /pokemons/random`
- Resultat attendu:
  - HTTP 200
  - Liste de 3 elements
  - Chaque element contient `api_id`, `name`, `stats`
  - `stats` contient 6 attributs attendus

## CT-03 - Creation trainer
- Priorite: P2
- Type: CRUD
- Pre-conditions: base SQLite accessible
- Entree: `POST /trainers/` avec body JSON valide
- Resultat attendu:
  - HTTP 200
  - Objet trainer cree avec `id`

## CT-04 - Battle negatif (ID invalide)
- Priorite: P1
- Type: API negatif
- Pre-conditions: API lancee
- Entree: `GET /pokemons/battle?first_api_id=-1&second_api_id=4`
- Resultat attendu:
  - HTTP erreur (502 ou 4xx selon implementation)
  - Message d'erreur explicite
