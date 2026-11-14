# PFA 07 – Reconnaissance intelligente des maladies végétales (tomate)

Apprentissage profond et vision artificielle embarquée – EMSI, cycle ingénieur, 2026-2027.
**Étudiants :** AMEUR EL IDRISSI Aymane, BELAYACHI Adnane – **Encadrant :** Dr. Mohammed MESTARI.

Ce dépôt contient les **scripts, notebooks et fichiers de preuve** du jalon S2 (données, audit, partitions sans fuite). Les **images des corpus ne sont pas redistribuées** (licences, volume) : elles se récupèrent aux révisions indiquées ci-dessous.

## 1. Contenu du dépôt

| Élément | Rôle |
|---|---|
| `audit_corpusPV.ipynb` | Audit du corpus PlantVillage (inventaire, doublons, qualité, classes) |
| `audit_corpusPD.ipynb` | Audit du corpus PlantDoc(inventaire, doublons, qualité, classes) |
| `restore_invalid_names.py` | Restaure sous un nom assaini les fichiers dont le nom est interdit sous Windows |
| `partitions_plantvillage.ipynb` | Partitions entraînement / validation / test **par feuille**, contrôles anti-fuite |
| `contamination_plantvillage_plantdoc.ipynb` | Recherche de copies de PlantVillage dans le test externe PlantDoc |
| `conditions_s2_plantvillage.ipynb` | Cohorte retenue et réserve, dépendance source–classe, sensibilité du seuil dHash |
| `checksums.py` | Génère et vérifie les empreintes SHA-256 des artefacts et les révisions des corpus |
| `DATA_REVISIONS.json` | Révisions (commits) et effectifs attendus des corpus |
| `requirements.txt` | Dépendances Python |
| `audit/pv`, `audit/pd` | Sorties d'audit : `manifest.csv`, `exclusion_log.csv`, `class_mapping.csv`, `audit_config.json`, `audit_report.md`… |
| `audit/pd/restored_files.csv` | Traçabilité des fichiers restaurés (nom d'origine, nom restauré, SHA-256) |
| `partitions/pv` | `partition.csv`, `train.csv`, `val.csv`, `test.csv`, `groups.csv`, `reserve_non_cartographiee.csv`, `partition_report.md` |
| `contamination`, `conditions_s2` | Sorties des deux autres notebooks (dont `decision_reserve.md`) |
| `CHECKSUMS.sha256` | Empreintes attendues des artefacts |

Les notebooks se lancent **depuis la racine du dépôt** : les chemins de leur cellule de configuration sont relatifs à cette racine.

## 2. Prérequis

- Python 3.9 ou plus récent, Git.
- `pip install -r requirements.txt` (de préférence dans un environnement virtuel).

## 3. Reproduire l'audit et les partitions

### Étape 1 – Récupérer les corpus aux révisions exactes (tomate uniquement)

```bash
git clone --filter=blob:none --no-checkout https://github.com/spMohanty/PlantVillage-Dataset
cd PlantVillage-Dataset
git sparse-checkout init --no-cone
git sparse-checkout set "/leaf_grouping/" "/raw/color/Tomato*/"
git checkout 7f7ecc7e1eaca78107e3affe7cb5abd9427e139a
cd ..

git clone --filter=blob:none --no-checkout https://github.com/pratikkayal/PlantDoc-Dataset
cd PlantDoc-Dataset
git sparse-checkout init --no-cone
git sparse-checkout set "/train/Tomato*/" "/test/Tomato*/" "/LICENSE.txt" "/README.md"
git checkout 5467f6012d78d1c446145d5f582da6096f852ae8
cd ..
```

**Windows uniquement :** `git checkout` signale des erreurs `invalid path` pour les fichiers de PlantDoc dont le nom contient « ? ». Restaurez-les :

```bash
python restore_invalid_names.py --repo PlantDoc-Dataset --log audit/pd/restored_files.csv --all-missing
```

### Étape 2 – Vérifier les corpus

```bash
python checksums.py datasets
```

Chaque ligne doit afficher `OK` (révision et effectifs par classe).

### Étape 3 – Exécuter les notebooks dans cet ordre

| N° | Notebook | Configuration à renseigner | Sorties |
|---|---|---|---|
| 1 | `audit_corpusPV.ipynb` | `CORPUS="plantvillage"`, `ROOT=Path("PlantVillage-Dataset/raw/color")`, `OUT=Path("audit/pv")`, `REVISION` | `audit/pv/` |
| 2 | `audit_corpusPD.ipynb` | `CORPUS="plantdoc"`, `ROOT=Path("PlantDoc-Dataset")`, `OUT=Path("audit/pd")`, `REVISION` | `audit/pd/` |
| 3 | `partitions_plantvillage.ipynb` | Valeurs par défaut (graine 42) | `partitions/pv/` |
| 4 | `contamination_plantvillage_plantdoc.ipynb` | Valeurs par défaut | `contamination/` |
| 5 | `conditions_s2_plantvillage.ipynb` | Valeurs par défaut (graine 42) | `conditions_s2/` |

Après l'étape 1 ou 2, **ouvrir `class_mapping.csv`**, valider les classes (statut `CONFIRME`) puis relancer l'audit : la correspondance validée est conservée.

### Étape 4 – Vérifier les artefacts

```bash
python checksums.py generate    # une seule fois, après la remise des preuves
python checksums.py verify      # à chaque contrôle
python checksums.py all         # artefacts + corpus
```

Les empreintes ignorent les champs volatils (dates, versions, plateforme), les fins de ligne et les sorties des notebooks : une réexécution identique doit donner `OK` partout. Un fichier `MODIFIÉ` indique une différence de contenu à expliquer.

## 4. Résultats attendus (contrôle rapide)

| Étape | Indicateur | Valeur attendue |
|---|---|---|
| Audit PlantVillage | Images de tomate inventoriées / exclues / conservées (cinq classes) | 18 160 / 14 / 7 209 |
| Audit PlantVillage | Empreinte du manifeste (début) | `2b3bbacc616c75f9…` |
| Audit PlantDoc | Images inventoriées / exclues / conservées (cinq classes) | 746 / 4 / 502 |
| Audit PlantDoc | Empreinte du manifeste (début) | `0b01ff265dd70574…` |
| Partitions | Images partitionnées / groupes / réserve | 4 870 / 1 218 / 2 339 |
| Partitions | Contrôles anti-fuite | Tous réussis |
| Conditions S2 | V de Cramér source–classe (images incluses) | environ 1,00 |
| Conditions S2 | Paires de quasi-doublons à distance ≤ 4 dans la cohorte | 0 |

*Tableau 1 – Valeurs de référence du jalon S2 (graine 42).*

## 5. Règles du protocole

- **PlantDoc n'est jamais utilisé** pour entraîner, choisir un modèle, un hyperparamètre ou un seuil : test externe seulement.
- Les **partitions** sont définies au niveau des feuilles, avant toute augmentation ; les feuilles reliées par un quasi-doublon (dHash 64 bits, distance de Hamming ≤ 4) ou un fichier identique sont fusionnées.
- Les **2 339 images sans identifiant de feuille** sont exclues de l'apprentissage, de la validation et du test interne (voir `conditions_s2/decision_reserve.md`).
- **Graine fixe** : 42.

## 6. Limites connues

- Dans la cohorte partitionnée, chaque classe provient d'une seule source d'acquisition (V de Cramér ≈ 1) : le test interne ne prouve pas la généralisation à de nouvelles conditions de collecte.
- Le dHash ne détecte pas les recadrages importants ; les retournements et rotations sont contrôlés séparément.
- Le regroupement par feuille suppose l'exactitude de `leaf-map.json`.

## 7. Licences et données

- PlantDoc : CC BY 4.0 (voir le dépôt d'origine).
- PlantVillage : (voir le dépôt d'origine).
- Ce dépôt ne redistribue aucune image des corpus.
