# Annexe - Evaluation des risques (sans matrice)

## R1 - PokeAPI indisponible / rate-limit
- Probabilite: moyenne
- Impact: eleve
- Effet: endpoints battle/random en erreur
- Action: fallback mock en test, retries limites, message d'erreur explicite

## R2 - Regressions apres correction
- Probabilite: moyenne
- Impact: eleve
- Effet: fonctionnalites existantes cassees
- Action: execution systematique `pytest` + revue de code

## R3 - Instabilite des tests (flaky)
- Probabilite: faible a moyenne
- Impact: moyen
- Effet: faux positifs/faux negatifs
- Action: isoler avec mocks, figer les donnees de test

## R4 - Resultats de charge non reproductibles
- Probabilite: moyenne
- Impact: moyen
- Effet: comparaison difficile entre campagnes
- Action: standardiser scenario Locust (users, spawn rate, duree, host)
