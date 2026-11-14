# Rapport d'audit - plantvillage

*Généré le 2026-11-07T20:06:20+00:00 UTC - révision du corpus : spMohanty/PlantVillage-Dataset, commit 7f7ecc7e1eaca78107e3affe7cb5abd9427e139a téléchargé le 2026-11-06 - empreinte du manifeste : `2b3bbacc616c75f9...`*

## Synthèse
- Images inventoriées : **18160** ; illisibles : **0** ; exclues : **14** ; conservées dans le périmètre : **7209**.
- Groupes de quasi-doublons à examiner : **33**.

## Effectifs par classe
| class_origin | class_retained | class_status | n_scannees | n_illisibles | n_exclues | n_conservees | n_en_cluster_quasi_doublon |
|---|---|---|---|---|---|---|---|
| Tomato___Bacterial_spot | hors_perimetre | CONFIRME | 2127 | 0 | 0 | 2127 | 5 |
| Tomato___Early_blight | alternariose_precoce | CONFIRME | 1000 | 0 | 0 | 1000 | 1 |
| Tomato___Late_blight | mildiou_tardif | CONFIRME | 1909 | 0 | 8 | 1901 | 5 |
| Tomato___Leaf_Mold | cladosporiose | CONFIRME | 952 | 0 | 0 | 952 | 0 |
| Tomato___Septoria_leaf_spot | septoriose | CONFIRME | 1771 | 0 | 0 | 1771 | 0 |
| Tomato___Spider_mites Two-spotted_spider_mite | hors_perimetre | CONFIRME | 1676 | 0 | 0 | 1676 | 1 |
| Tomato___Target_Spot | hors_perimetre | CONFIRME | 1404 | 0 | 0 | 1404 | 1 |
| Tomato___Tomato_Yellow_Leaf_Curl_Virus | hors_perimetre | CONFIRME | 5357 | 0 | 0 | 5357 | 37 |
| Tomato___Tomato_mosaic_virus | hors_perimetre | CONFIRME | 373 | 0 | 0 | 373 | 2 |
| Tomato___healthy | saine | CONFIRME | 1591 | 0 | 6 | 1585 | 15 |

*Tableau 1 - Effectifs avant et après nettoyage.*

## Motifs d'exclusion
| motif | n |
|---|---|
| doublon_exact_de | 14 |

*Tableau 2 - Exclusions par motif.*

## Résolutions et formats
| class_origin | larg_min | larg_med | larg_max | haut_min | haut_med | haut_max | formats |
|---|---|---|---|---|---|---|---|
| Tomato___Bacterial_spot | 256 | 256.0 | 256 | 256 | 256.0 | 256 | JPEG:2127 |
| Tomato___Early_blight | 256 | 256.0 | 256 | 256 | 256.0 | 256 | JPEG:1000 |
| Tomato___Late_blight | 256 | 256.0 | 256 | 256 | 256.0 | 256 | JPEG:1909 |
| Tomato___Leaf_Mold | 256 | 256.0 | 256 | 256 | 256.0 | 256 | JPEG:952 |
| Tomato___Septoria_leaf_spot | 256 | 256.0 | 256 | 256 | 256.0 | 256 | JPEG:1771 |
| Tomato___Spider_mites Two-spotted_spider_mite | 256 | 256.0 | 256 | 256 | 256.0 | 256 | JPEG:1676 |
| Tomato___Target_Spot | 256 | 256.0 | 256 | 256 | 256.0 | 256 | JPEG:1404 |
| Tomato___Tomato_Yellow_Leaf_Curl_Virus | 256 | 256.0 | 256 | 256 | 256.0 | 256 | JPEG:5357 |
| Tomato___Tomato_mosaic_virus | 256 | 256.0 | 256 | 256 | 256.0 | 256 | JPEG:373 |
| Tomato___healthy | 256 | 256.0 | 256 | 256 | 256.0 | 256 | JPEG:1591 |

*Tableau 3 - Dimensions et formats par classe.*

## Qualité et uniformité du fond
| class_origin | lum_med | contraste_med | flou_lapvar_med | fond_border_std_med |
|---|---|---|---|---|
| Tomato___Bacterial_spot | 102.96 | 32.73 | 584.43 | 23.25 |
| Tomato___Early_blight | 109.09 | 44.96 | 1037.25 | 32.83 |
| Tomato___Late_blight | 118.49 | 39.65 | 852.52 | 26.55 |
| Tomato___Leaf_Mold | 116.46 | 34.76 | 1308.64 | 22.41 |
| Tomato___Septoria_leaf_spot | 127.94 | 35.87 | 1638.06 | 21.01 |
| Tomato___Spider_mites Two-spotted_spider_mite | 120.13 | 41.02 | 2098.3 | 27.13 |
| Tomato___Target_Spot | 118.89 | 41.7 | 2180.47 | 31.69 |
| Tomato___Tomato_Yellow_Leaf_Curl_Virus | 113.44 | 33.42 | 526.32 | 21.45 |
| Tomato___Tomato_mosaic_virus | 118.83 | 30.99 | 1644.56 | 19.49 |
| Tomato___healthy | 116.68 | 35.62 | 3419.08 | 25.35 |

*Tableau 4 - Médianes par classe (luminance, contraste, flou, border_std).*

## Correspondances à valider
| class_origin | class_retained | status |
|---|---|---|

*Tableau 5 - Classes dont le statut n'est pas encore CONFIRME.*


## Règle de décision
Les images quasi identiques (distance de Hamming ≤ 4 sur un dHash de 64 bits) sont regroupées en clusters après examen visuel ; aucune image n’est supprimée, mais tous les membres d’un même cluster sont affectés à une seule partition (entraînement, validation ou test) afin d’éviter toute fuite de données.