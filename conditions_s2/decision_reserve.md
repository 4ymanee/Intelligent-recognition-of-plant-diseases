# Décision sur les images sans identifiant de feuille

*Généré le 2026-11-12T20:36:42+00:00 UTC - graine 42*

## Constat
- Images éligibles : **7209** ; incluses (groupes de feuilles) : **4870** ; réservées : **2339** (32.4 %).
- La part réservée varie de **0.0 %** à **51.6 %** selon la classe (Tableau 1) : l'exclusion n'est pas aléatoire.
- Dépendance source–classe (V de Cramér) : **1.0** sur les images incluses, **1.0** sur l'ensemble éligible.
- Écarts notables incluses/réservées : **7** comparaison(s) classe × métrique sur 12.

## Décision proposée
1. La **cohorte principale** est constituée des 4870 images dotées d'un identifiant de feuille (`included.csv`). Le corpus d'apprentissage n'est plus décrit comme « 7 209 images ».
2. Les 2339 images réservées (`reserved.csv`) sont **exclues de l'apprentissage, de la validation, du test interne et de tout choix d'hyperparamètre ou de seuil**.
3. Usage autorisé des réserves : **description exploratoire** ou **étude de sensibilité distincte**, déclarée comme exploratoire.
4. **Aucune réintégration** après gel des partitions sans nouvelle expérience déclarée et nouveau manifeste versionné.
5. Limite à consigner : la cohorte principale n'est pas un échantillon aléatoire des images éligibles (couverture et sources différentes selon les classes).

Décision validée le [12/11/2026] par AMEUR EL IDRISSI Aymane et BELAYACHI Adnane ; version du dépôt : tag s2-artefacts-v1 »
