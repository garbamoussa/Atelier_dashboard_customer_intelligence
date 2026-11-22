# Atelier pratique – Premier dashboard Customer Intelligence

## Projet
Construction guidée d'un tableau de bord complet à partir du fichier e-commerce `online_retail.csv`, avec Python, Pandas, Plotly, Streamlit et une bibliothèque de prompts couvrant les cours du module.

## Jeu de données
Le fichier contient 541 909 lignes et 8 colonnes :
`InvoiceNo`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `UnitPrice`, `CustomerID`, `Country`.

Premiers constats d'audit :
- 4 372 identifiants clients distincts renseignés ;
- 25 900 numéros de facture distincts ;
- 38 pays ;
- 135 080 lignes avec `CustomerID` manquant ;
- 5 268 doublons exacts ;
- 1 454 descriptions manquantes ;
- 10 624 quantités négatives ;
- 2 517 prix nuls ou négatifs ;
- 9 288 factures dont le numéro commence par C ;
- période observée : 1 décembre 2010 au 9 décembre 2011.

## Architecture

```text
atelier_dashboard_customer_intelligence/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   └── online_retail.csv
├── prompts/
│   └── bibliotheque_prompts.md
└── src/
    ├── __init__.py
    └── data_quality.py
```

## Lancer le dashboard

Python 3.10+ :

```bash
python -m venv .venv
```

Windows PowerShell :
```powershell
.venv\Scripts\Activate.ps1
```

Git Bash / macOS / Linux :
```bash
source .venv/bin/activate
```

Puis :
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Règles métier provisoires du dashboard

- CA affiché = somme de `Quantity × UnitPrice` sur les lignes positives, hors factures d'annulation et prix non positifs.
- Les quantités négatives et les factures d'annulation sont conservées pour l'analyse séparée des retours/annulations.
- Les clients sans `CustomerID` peuvent contribuer au CA global, mais ne sont pas inclus dans les analyses individuelles et RFM.
- Panier moyen = CA retenu / nombre de numéros de facture distincts dans le périmètre.
- La devise affichée est £, conformément au contexte habituel de ce jeu de données, mais elle doit être confirmée avec le producteur des données.

Ces règles sont des choix pédagogiques explicites, à faire valider par le métier avant usage opérationnel. Le CA calculé est brut : il ne représente ni marge ni bénéfice.

## Parcours pédagogique aligné sur les cours

| Séquence | Cours mobilisé | Travail étudiant | Livrable |
|---|---|---|---|
| 1 | Collecte et sourcing | Décrire source, périmètre, granularité, dictionnaire | Fiche dataset |
| 2 | Prompt engineering | Utiliser prompts de diagnostic et de préparation | Journal de prompts |
| 3 | Préparation des données | Auditer, nettoyer avec règles tracées | Script + rapport qualité |
| 4 | EDA | Étudier distributions, tendances, pays, produits, clients | Notebook EDA |
| 5 | Prompt analyse | Calculer KPI, comparer segments, RFM | Note d'analyse |
| 6 | Dataviz | Choisir et justifier les graphiques | Graphiques commentés |
| 7 | Prompt formatage/visualisation | Générer un plan de dashboard | Maquette |
| 8 | Looker Studio / Streamlit | Construire filtres, KPI, graphiques | Dashboard interactif |
| 9 | Data communication | Reporting et storytelling | Rapport de synthèse |
| 10 | Évaluation IA | Vérifier code, chiffres, biais et hallucinations | Grille de validation |
| 11 | Optimisation | Tester exactitude, performance et ergonomie | Version améliorée |
| 12 | GitHub | Versionner code, README, prompts et livrables | Dépôt GitHub |

## Mission étudiante

Vous êtes une équipe Customer Intelligence mandatée par une enseigne e-commerce. Construisez un tableau de bord permettant de répondre à ces questions :
1. Comment évoluent les ventes au fil du temps ?
2. Quels pays et produits contribuent le plus au chiffre d'affaires ?
3. Quels clients identifiés génèrent le plus de valeur ?
4. Quels clients sont récents, fréquents ou à réactiver selon une analyse RFM ?
5. Quelle est l'importance des retours et annulations ?
6. Quelles limites empêchent de calculer la rentabilité et la performance d'acquisition ?

### Livrables
- dépôt GitHub documenté ;
- rapport de qualité des données ;
- notebook EDA ;
- bibliothèque de prompts et journal des itérations ;
- dashboard Streamlit ;
- rapport de 1 à 2 pages ;
- 3 constats, 3 recommandations et plan de mesure ;
- note de vérification des résultats générés par IA.

## Barème indicatif

| Critère | Points |
|---|---:|
| Compréhension du dataset et sourcing | 10 |
| Qualité des données et transformations | 15 |
| EDA et calcul des KPI | 15 |
| Qualité des prompts et itérations | 10 |
| Datavisualisation et dashboard | 20 |
| Analyse, storytelling et recommandations | 15 |
| Vérification critique des sorties IA | 10 |
| GitHub, documentation et reproductibilité | 5 |
| **Total** | **100** |

## Limites et points de vigilance
- Le jeu de données ne contient ni coût d'achat, ni marge, ni coûts marketing, ni sessions web, ni exposition aux campagnes. Il ne permet donc pas de calculer un bénéfice, un ROAS, un CPA ou un taux de conversion marketing.
- Les `CustomerID` manquants sont nombreux : ne pas leur attribuer un identifiant client artificiel pour le RFM.
- Les doublons exacts doivent être étudiés avant suppression.
- Les retours et annulations doivent être distingués des ventes positives.
- Les données historiques s'arrêtent au 9 décembre 2011 : ne pas présenter ce jeu comme une représentation du marché actuel.
- Les prompts servent à accélérer le travail, pas à remplacer les calculs reproductibles ni la validation métier.
