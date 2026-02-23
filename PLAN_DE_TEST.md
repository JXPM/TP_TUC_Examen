# Plan de test - TP TUC Examen

## 1. Ressources impliquees
### 1.1 Ressources humaines
- 1 developpeur/testeur principal (preparation, execution, correction)
- 1 relecteur (validation finale des resultats)

### 1.2 Ressources techniques
- Poste Linux avec Python 3.10
- API FastAPI (`uvicorn main:app --reload`)
- Base SQLite (`sqlite.db`)
- Outils: `pytest`, `coverage`, `locust`, `pylint`
- Connexion internet (appel PokeAPI)

### 1.3 Livrables de test
- Rapport d'execution (`pytest -q`)
- Rapport de couverture (`coverage report -m`)
- Resultats de charge Locust
- Ce plan de test (`PLAN_DE_TEST.md`)

## 2. Besoins pour realiser les activites de test
- Environnement Python installe avec dependances (`requirements.txt`)
- API demarrable localement sur `http://127.0.0.1:8000`
- Acces a PokeAPI (`https://pokeapi.co/api/v2`)
- Jeu de donnees minimal en base (trainers/pokemons) pour les tests CRUD
- Disponibilite d'un terminal pour lancer les campagnes (`pytest`, `locust`)

## 3. Facteurs d'effort de test
L'effort de test depend principalement du nombre d'endpoints a couvrir, de la dependance a une API externe (PokeAPI), de la necessite de maintenir des mocks fiables pour eviter les tests instables, et du temps d'investigation quand un defaut est lie a l'infrastructure (reseau, service externe, environnement local). La charge augmente aussi avec les exigences qualite (coverage minimum, note pylint minimale, tests de charge) qui imposent des executions supplementaires et des corrections iteratives.

## 4. KPIs de suivi (3)
- KPI-1: **Taux de tests passes** = (tests passes / tests executes) * 100
  - Cible: 100% avant rendu
- KPI-2: **Couverture de code** (coverage global)
  - Cible: >= 85% (groupe 4) ou >= 80% (groupe 3)
- KPI-3: **Taux d'erreur en charge** (Locust)
  - Cible: < 5% d'erreurs sur le scenario nominal

## 5. Budget (couts potentiels)
- Temps humain (principal cout): conception, execution, correction, re-tests
- Infrastructure: machine de test dediee si charge plus lourde
- Reseau/API externe: indisponibilite PokeAPI pouvant imposer des reprises de test
- Outils CI/CD (si usage cloud prive): minutes de build/test facturables

## 6. Cas de test
Les cas detailles sont fournis en annexe dans `ANNEXE_CAS_DE_TEST.md`.

Extrait minimum (4 cas dont 1 negatif):
- CT-01 (positif): Battle entre 2 IDs valides (`/pokemons/battle?first_api_id=1&second_api_id=4`) -> winner renseigne ou egalite valide
- CT-02 (positif): Endpoint random (`/pokemons/random`) -> 3 pokemons + stats completes
- CT-03 (positif): Creation trainer -> insertion reussie + id retourne
- CT-04 (negatif): Battle avec ID invalide (`/pokemons/battle?first_api_id=-1&second_api_id=4`) -> erreur HTTP attendue (502 ou 4xx selon gestion)

## 7. Evaluation des risques (sans matrice, comme demande)
Le detail est fourni en annexe `ANNEXE_RISQUES.md` avec 4 risques:
- R1: Indisponibilite/rate-limit PokeAPI
- R2: Regressions fonctionnelles lors de modifications
- R3: Instabilite des tests due aux dependances externes
- R4: Resultats de performance non reproductibles selon machine

## 8. Criteres d'entree et de sortie
### 8.1 Critere d'entree
- Code compile et API demarrable sans erreur
- Dependances installees
- Scenarios de test valides et cas de test prets
- Acces PokeAPI ou mocks disponibles

### 8.2 Critere de sortie
- Tous les tests critiques passes
- KPI-1 atteint (100% tests verts sur campagne finale)
- KPI-2 atteint (coverage conforme au groupe)
- KPI-3 respecte sur scenario de charge nominal
- Defauts bloquants corriges ou explicitement acceptes

## 9. Planification, priorisation et dependances
Priorisation des cas:
1. P1 - CT-01 Battle valide (coeur de l'examen)
2. P1 - CT-04 Battle negatif (robustesse)
3. P1 - CT-02 Random + stats
4. P2 - CT-03 Creation trainer

Dependances:
- CT-01 depend de la disponibilite PokeAPI (ou mock)
- CT-04 depend de la route battle operationnelle
- CT-02 depend de la route random et de l'extraction des stats
- CT-03 depend de la base SQLite accessible

## 10. Annexes
- `ANNEXE_CAS_DE_TEST.md` (cas de test detailles)
- `ANNEXE_RISQUES.md` (registre des risques, 4 risques, sans matrice)

## 11. Comment obtenir les pourcentages et indicateurs
### 11.1 Pourcentage de tests passes
Commande:
```bash
pytest -q
```
Lecture:
- Le resume final indique le nombre de tests passes/echoues.
- Le taux de succes se calcule avec: `(passes / total) * 100`.
## 11. Resultats de campagne de test (constates)
### 11.1 Resultat tests unitaires
- 10 tests executes
- 10 tests passes
- 0 test en echec
- Taux de succes: 100%
- Temps d'execution observe: 0.82s
 
### 11.2 Pourcentage de couverture de code
Commandes:
```bash
-test__venv/bin/coverage run -m pytest -q
-test__venv/bin/coverage report -m
```
Lecture:
- La ligne `TOTAL` donne le pourcentage global de couverture.
- Chaque fichier a aussi son propre pourcentage.
### 11.2 Resultat couverture de code
| Fichier | Couverture |
| app/__init__.py | 100% |
| app/actions.py | 67% |
| app/models.py | 100% |
| app/routers/__init__.py | 100% |
| app/routers/pokemons.py | 91% |
| app/schemas.py | 100% |
| app/sqlite.py | 100% |
| app/utils/__init__.py | 100% |
| app/utils/pokeapi.py | 93% |
| app/utils/utils.py | 50% |
| tests/conftest.py | 80% |
| tests/test_pokeapi.py | 100% |
| tests/test_routes_and_actions.py | 100% |
 