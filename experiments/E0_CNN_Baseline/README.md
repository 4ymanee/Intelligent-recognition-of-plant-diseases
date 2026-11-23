# E0 — CNN Baseline

## 1. Présentation

Cette expérience constitue la première étape expérimentale du projet **« Reconnaissance intelligente des maladies végétales par apprentissage profond et vision artificielle embarquée »**.

L'objectif de E0 est de développer une architecture CNN (*Convolutional Neural Network*) de référence, entraînée à partir de zéro (*from scratch*), afin d'évaluer sa capacité à reconnaître cinq catégories d'images de feuilles de tomate.

Cette baseline servira de référence pour les expérimentations ultérieures portant sur l'amélioration de l'architecture, les stratégies d'apprentissage et l'optimisation du modèle pour son déploiement embarqué.

## 2. Jeu de données

L'expérience utilise une partition contrôlée du jeu de données **PlantVillage**, définie lors de la phase de préparation des données.

| Partition | Nombre d'images | Proportion |
|---|---:|---:|
| Entraînement | 3 418 | 70,18 % |
| Validation | 732 | 15,03 % |
| Test interne | 720 | 14,78 % |
| **Total** | **4 870** | **100 %** |

### Classes étudiées

Le modèle distingue les cinq classes suivantes :

1. `alternariose_precoce`
2. `cladosporiose`
3. `mildiou_tardif`
4. `saine`
5. `septoriose`

### Prétraitement

- Redimensionnement des images en 224 × 224 pixels.
- Conversion en trois canaux RGB.
- Normalisation des pixels dans l'intervalle [0, 1].
- Encodage des classes sous forme d'entiers.
- Absence d'augmentation artificielle des données pour cette baseline.

Les partitions d'entraînement, de validation et de test interne sont utilisées conformément au protocole expérimental défini en amont.

**Important :** PlantDoc est réservé à l'évaluation externe E5. Il n'est pas utilisé pour entraîner le modèle, sélectionner l'architecture ou ajuster les hyperparamètres.

## 3. Architecture du modèle

Le modèle `CNN_E0` est un réseau convolutif compact composé de trois blocs convolutifs.

| Couche | Configuration |
|---|---|
| Entrée | 224 × 224 × 3 |
| Bloc convolutif 1 | Conv2D (32 filtres) + BatchNormalization + ReLU + MaxPooling |
| Bloc convolutif 2 | Conv2D (64 filtres) + BatchNormalization + ReLU + MaxPooling |
| Bloc convolutif 3 | Conv2D (128 filtres) + BatchNormalization + ReLU + MaxPooling |
| Agrégation | GlobalAveragePooling2D |
| Couche dense | 128 neurones + ReLU |
| Régularisation | Dropout (0,3) |
| Sortie | 5 neurones + Softmax |

### Nombre de paramètres

- Paramètres totaux : **111 301**
- Paramètres entraînables : **110 853**
- Paramètres non entraînables : **448**

## 4. Configuration d'entraînement

| Paramètre | Valeur |
|---|---|
| Optimiseur | Adam |
| Learning rate | 0,001 |
| Fonction de perte | Sparse Categorical Crossentropy |
| Batch size | 32 |
| Nombre maximal d'époques | 50 |
| Nombre d'époques effectuées | 27 |
| Early stopping | Patience de 8 époques |
| Graine aléatoire | 42 |
| Métrique de sélection | Validation Macro-F1 |

Le meilleur modèle est sélectionné selon le **Macro-F1 sur l'ensemble de validation**. Les poids correspondant à la meilleure époque sont restaurés avant l'évaluation finale.

## 5. Résultats expérimentaux

### 5.1. Validation

Le meilleur résultat de validation est obtenu à l'époque 19.

| Métrique | Résultat |
|---|---:|
| Validation Accuracy | 94,95 % |
| Validation Macro-F1 | 94,85 % |
| Validation Loss | 0,1444 |
| Meilleure époque | 19 / 27 |

### 5.2. Test interne

L'évaluation finale est réalisée sur les 720 images du test interne.

| Métrique | Résultat |
|---|---:|
| Test Accuracy | 95,28 % |
| Test Macro-F1 | 95,21 % |
| Macro Precision | 95,32 % |
| Macro Recall | 95,17 % |
| Weighted F1-score | 95,26 % |

### 5.3. Résultats par classe

| Classe | Precision | Recall | F1-score |
|---|---:|---:|---:|
| alternariose_precoce | 93,33 % | 94,59 % | 93,96 % |
| cladosporiose | 97,74 % | 92,86 % | 95,24 % |
| mildiou_tardif | 94,62 % | 90,44 % | 92,48 % |
| saine | 97,37 % | 100,00 % | 98,67 % |
| septoriose | 93,55 % | 97,97 % | 95,71 % |

### 5.4. Matrice de confusion

Les lignes correspondent aux classes réelles et les colonnes aux classes prédites.

| Réel / Prédit | Alternariose | Cladosporiose | Mildiou | Saine | Septoriose |
|---|---:|---:|---:|---:|---:|
| Alternariose | 140 | 0 | 6 | 0 | 2 |
| Cladosporiose | 0 | 130 | 1 | 3 | 6 |
| Mildiou | 10 | 0 | 123 | 1 | 2 |
| Saine | 0 | 0 | 0 | 148 | 0 |
| Septoriose | 0 | 3 | 0 | 0 | 145 |

### 5.5. Analyse

Le modèle obtient un Macro-F1 de 95,21 % sur le test interne, indiquant de bonnes performances sur la partition PlantVillage utilisée.

La classe `saine` présente le meilleur résultat, avec un rappel de 100 %. La classe `mildiou_tardif` constitue la principale difficulté, avec un rappel de 90,44 %.

Les confusions les plus importantes concernent :
- Le mildiou prédit comme alternariose précoce : 10 images.
- La cladosporiose prédite comme septoriose : 6 images.
- L'alternariose précoce prédite comme mildiou : 6 images.

Ces résultats constituent une première référence pour les comparaisons expérimentales ultérieures.

## 6. Test de capacité de mémorisation

Avant l'entraînement complet, un test de surapprentissage contrôlé (*small-batch overfit test*) a été réalisé sur un sous-ensemble de 32 images.

Après 30 époques :
- Accuracy maximale observée : 90,62 %.
- Loss minimale observée : 0,5223.

Ce test confirme que le pipeline d'apprentissage et l'architecture sont capables de mémoriser un petit sous-ensemble de données.

## 7. Limites et précautions d'interprétation

Les performances obtenues ne démontrent pas à elles seules la capacité du modèle à généraliser à des images prises dans des conditions réelles de culture.

L'analyse de dépendance entre les classes et les sources de données, réalisée lors de la phase précédente, a mis en évidence une forte association entre ces deux variables. Cette dépendance constitue une limite importante de l'évaluation interne sur PlantVillage.

Par conséquent :
- Les résultats E0 doivent être interprétés comme une référence expérimentale interne.
- Le test interne ne doit pas être réutilisé pour ajuster les hyperparamètres.
- PlantDoc reste réservé à l'évaluation externe prévue en E5.
- Les expérimentations suivantes devront examiner la robustesse et la généralisation du modèle.

## 8. Artefacts produits

| Fichier | Description |
|---|---|
| `best_e0.keras` | Modèle Keras de référence sélectionné sur validation |
| `best_e0.weights.h5` | Poids du meilleur modèle |
| `e0_config.json` | Configuration et paramètres de l'expérience |
| `training_log.csv` | Historique des métriques d'entraînement et de validation |

Le notebook associé est conservé dans `notebooks/PFA_E0_CNN_Baseline.ipynb`.

## 9. Environnement expérimental

- Plateforme : Google Colab
- Framework : TensorFlow 2.21.0
- Accélération : GPU disponible
- Langage : Python
- Bibliothèques complémentaires : NumPy, Pandas, Scikit-learn, Matplotlib et Seaborn

## 10. Conclusion et prochaines étapes

L'expérience E0 a permis de construire et d'évaluer une première architecture CNN de référence sur les cinq classes de maladies de la tomate.

Le modèle atteint un Macro-F1 de 95,21 % sur le test interne PlantVillage. Ces résultats constituent le point de comparaison pour les expérimentations suivantes.

Les prochaines étapes porteront notamment sur :

1. La comparaison de plusieurs architectures CNN.
2. L'étude de stratégies d'augmentation des données.
3. L'amélioration de la généralisation du modèle.
4. L'analyse de la robustesse face aux perturbations.
5. L'étude de la quantification et du déploiement sur une plateforme embarquée.

---