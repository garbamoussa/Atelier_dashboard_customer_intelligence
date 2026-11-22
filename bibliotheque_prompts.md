# Bibliothèque de prompts – Atelier Customer Intelligence

**Mode d'emploi :** les prompts ci-dessous sont à utiliser avec un LLM en joignant le CSV ou un extrait représentatif. Pour 541 909 lignes, ne pas coller tout le fichier dans une conversation : demander du code Python exécutable sur le fichier local. Les résultats produits par l'IA doivent être recalculés ou contrôlés avec Pandas/SQL.

## Prompt 1 – Collecte et sourcing de l'information

> Tu es analyste data spécialisé en e-commerce. Examine les métadonnées et la structure du fichier `online_retail.csv`. Décris les colonnes, les types attendus, la granularité d'une ligne et les limites du périmètre. Distingue les faits observables des hypothèses. N'invente ni source, ni définition métier absente du fichier. Propose les questions à poser au propriétaire des données : devise, fuseau horaire, définition d'une facture, traitement des retours, signification des factures préfixées par C et origine des clients anonymes.

## Prompt 2 – Diagnostic de qualité des données

> Agis comme un Data Quality Analyst. Écris un script Python/Pandas qui audite `online_retail.csv` : dimensions, types, valeurs manquantes, doublons exacts, valeurs distinctes, dates invalides, quantités négatives, prix nuls/négatifs, factures dont le numéro commence par C, CustomerID manquants. Le script doit produire un rapport CSV. Ne supprime aucune ligne. Pour chaque anomalie, indique son volume, son risque métier et une règle de traitement à faire valider.

## Prompt 3 – Nettoyage et transformation

> Tu es Data Engineer. Propose un pipeline reproductible en Pandas pour parser `InvoiceDate` au format mois/jour/année, convertir les types, normaliser les chaînes et créer `LineRevenue = Quantity * UnitPrice`, `IsCancellation`, `Year`, `Month`, `YearMonth`. Conserve les colonnes originales, crée des colonnes dérivées et trace chaque transformation. Ne supprime pas les quantités négatives, les prix négatifs, les factures annulées ou les CustomerID manquants sans justification. Génère un script et des tests de contrôle.

## Prompt 4 – Exploration des données (EDA)

> Agis comme un Data Analyst e-commerce. À partir du fichier et sans inventer de résultats, construis un notebook EDA : profil des variables, qualité, distribution des quantités et prix, CA par mois, pays, produit et facture, analyse des annulations/retours et couverture des CustomerID. Pour chaque résultat, indique la formule, le dénominateur et le périmètre. Distingue les constats, hypothèses et questions ouvertes.

## Prompt 5 – Définition des KPI

> Tu es consultant Customer Intelligence. Construis un dictionnaire de KPI calculables avec les colonnes disponibles : CA brut des lignes positives, nombre de factures, clients identifiés, unités vendues, panier moyen par facture, CA par pays et produit, fréquence d'achat et récence client. Pour chaque KPI, fournis définition, formule, granularité, filtres, limites et exemple de code Pandas. Signale explicitement les KPI non calculables : marge, bénéfice, CLV complète, ROAS, CPA et taux de conversion marketing, faute de coûts, campagnes et données de navigation.

## Prompt 6 – Analyse clients et segmentation RFM

> Tu es CRM Data Analyst. Construis une analyse RFM sur les clients ayant un CustomerID renseigné. Récence = nombre de jours depuis la dernière facture observée ; Fréquence = nombre de factures distinctes ; Montant = somme des lignes de vente retenues. Propose des seuils de scoring, explique les choix, teste la sensibilité des segments et fournis un tableau de profils. N'attribue pas de valeur vie client prédictive sans modèle et horizon validés. Ne traite pas les clients anonymes comme des clients distincts.

## Prompt 7 – Choix des graphiques

> Agis comme expert en datavisualisation. À partir des objectifs suivants, recommande un graphique et justifie-le : évolution mensuelle du CA, top pays, top produits, distribution du CA par client, relation fréquence/CA, retours par mois. Précise dimensions, mesures, unités, tri, échelle et pièges de lecture. Évite les graphiques décoratifs et les axes trompeurs.

## Prompt 8 – Conception du dashboard

> Tu es un Product Designer BI et développeur Streamlit. Conçois un dashboard Customer Intelligence avec quatre espaces : vue d'ensemble, clients, produits, qualité des données. Ajoute filtres par pays et période, KPI en haut, graphiques cohérents, définitions des mesures, message sur les limites et export CSV. Le dashboard doit être lisible, accessible, réactif et ne pas afficher de données personnelles. Génère le code Python complet et explique comment le lancer.

## Prompt 9 – Data storytelling et reporting

> Tu es responsable de la performance e-commerce. À partir des agrégats calculés, rédige un reporting de direction structuré : faits clés, évolutions, écarts, segments et produits importants, limites, hypothèses à vérifier, recommandations et KPI de suivi. Chaque recommandation doit être reliée à un constat mesuré. N'affirme aucune causalité à partir d'une simple corrélation ou évolution temporelle.

## Prompt 10 – Recommandations marketing

> Tu es consultant marketing data. À partir des segments RFM, des pays et des produits les plus performants, propose des actions CRM et merchandising : réactivation, fidélisation, cross-sell, recommandations produits et priorisation géographique. Pour chaque action, précise cible, hypothèse, canal, coût à mesurer, KPI, groupe témoin éventuel et durée du test. Ne propose pas de ciblage individuel sur des identifiants ou coordonnées brutes.

## Prompt 11 – Vérification des réponses IA

> Agis comme auditeur indépendant. Vérifie le rapport et le code générés par une IA. Recalcule les KPI avec Pandas, contrôle les filtres, les doublons, les annulations, les valeurs manquantes, les agrégations et les dénominateurs. Liste les erreurs, hypothèses non justifiées, hallucinations potentielles et conclusions causales abusives. Donne pour chaque correction un test reproductible.

## Prompt 12 – Optimisation et mesure de performance

> Tu es expert en amélioration continue des dashboards. Évalue ce dashboard selon exactitude, pertinence métier, lisibilité, temps de chargement, interactivité et utilité décisionnelle. Propose un plan d'optimisation priorisé. Définis des critères de succès mesurables et des tests de non-régression pour garantir que les KPI ne changent pas involontairement.
