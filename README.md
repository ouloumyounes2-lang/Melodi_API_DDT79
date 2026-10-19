# API Melodi de l'Insee : test sur la base permanente des equipements

Test realise pour la DDT 79. Objectif : verifier si l'API Melodi de l'Insee
permet d'alimenter nos representations sans telechargement manuel de fichiers.

## Resultat du test

L'appel fonctionne. Pour les Deux-Sevres, l'API renvoie 9904 observations
couvrant les 252 communes du departement, millesime 2025.

| Domaine | Equipements |
|---|---|
| Services pour les particuliers | 6031 |
| Sante et action sociale | 3037 |
| Sports, loisirs et culture | 2008 |
| Commerces | 1761 |
| Enseignement | 519 |
| Tourisme | 155 |
| Transports et deplacements | 108 |

## Utilisation

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    python src/export_bpe.py

Les fichiers produits sont dans `outputs/`. Changer la variable DEP dans
`src/export_bpe.py` pour un autre departement.

## Points a connaitre

L'API ne demande ni compte ni cle. Elle est limitee a 30 requetes par minute et
a 100 000 lignes par requete (https://github.com/InseeFrLab/melodi).

Le jeu DS_BPE ne contient qu'un millesime a la fois. L'API sert donc toujours
la derniere version publiee par l'Insee, mais la mise a jour suit le rythme de
publication annuel de la BPE, pas davantage. Pour comparer plusieurs annees,
l'Insee diffuse un jeu separe, DS_BPE_EVOLUTION
(https://api.insee.fr/melodi/V2/catalog/all).

Les equipements sont classes sur trois niveaux : domaine, sous-domaine, type.
La classification compte 7 domaines, 27 sous-domaines et 209 types
(https://www.data.gouv.fr/datasets/base-permanente-des-equipements-2). La
modalite _T correspond au total, il faut la filtrer pour eviter les doubles
comptes.

Les communes sont identifiees par leur code Insee. Les libelles ne sont pas
repris ici, il faut les joindre depuis le COG
(https://www.insee.fr/fr/information/8377162).

## Sources

Documentation de l'API : https://portail-api.insee.fr/catalog/api/a890b735-159c-4c91-90b7-35159c7c9126/doc

Catalogue des jeux de donnees : https://catalogue-donnees.insee.fr