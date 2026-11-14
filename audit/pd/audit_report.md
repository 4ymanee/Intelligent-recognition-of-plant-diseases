# Rapport d'audit - plantdoc

*Généré le 2026-11-07T20:57:34+00:00 UTC - révision du corpus : pratikkayal/PlantDoc-Dataset, commit 5467f6012d78d1c446145d5f582da6096f852ae8 téléchargé le 2026-11-07 - empreinte du manifeste : `0b01ff265dd70574...`*

## Synthèse
- Images inventoriées : **746** ; illisibles : **0** ; exclues : **4** ; conservées dans le périmètre : **502**.
- Groupes de quasi-doublons à examiner : **23**.

## Effectifs par classe
| class_origin | class_retained | class_status | n_scannees | n_illisibles | n_exclues | n_conservees | n_en_cluster_quasi_doublon |
|---|---|---|---|---|---|---|---|
| Tomato Early blight leaf | alternariose_precoce | CONFIRME | 88 | 0 | 0 | 88 | 11 |
| Tomato Septoria leaf spot | septoriose | CONFIRME | 151 | 0 | 2 | 149 | 14 |
| Tomato leaf | saine | CONFIRME | 63 | 0 | 0 | 63 | 0 |
| Tomato leaf bacterial spot | hors_perimetre | CONFIRME | 110 | 0 | 1 | 109 | 6 |
| Tomato leaf late blight | mildiou_tardif | CONFIRME | 111 | 0 | 0 | 111 | 9 |
| Tomato leaf mosaic virus | hors_perimetre | CONFIRME | 54 | 0 | 0 | 54 | 1 |
| Tomato leaf yellow virus | hors_perimetre | CONFIRME | 76 | 0 | 1 | 75 | 4 |
| Tomato mold leaf | cladosporiose | CONFIRME | 91 | 0 | 0 | 91 | 1 |
| Tomato two spotted spider mites leaf | hors_perimetre | CONFIRME | 2 | 0 | 0 | 2 | 0 |

*Tableau 1 - Effectifs avant et après nettoyage.*

## Motifs d'exclusion
| motif | n |
|---|---|
| conflit_etiquette | 2 |
| doublon_exact_de | 2 |

*Tableau 2 - Exclusions par motif.*

## Résolutions et formats
| class_origin | larg_min | larg_med | larg_max | haut_min | haut_med | haut_max | formats |
|---|---|---|---|---|---|---|---|
| Tomato Early blight leaf | 150 | 599.0 | 3872 | 150 | 463.5 | 2592 | JPEG:88 |
| Tomato Septoria leaf spot | 143 | 600.0 | 6000 | 137 | 533.0 | 4000 | JPEG:150; PNG:1 |
| Tomato leaf | 401 | 1300.0 | 4000 | 273 | 1200.0 | 3780 | JPEG:63 |
| Tomato leaf bacterial spot | 150 | 600.0 | 4000 | 150 | 480.0 | 3000 | JPEG:110 |
| Tomato leaf late blight | 225 | 900.0 | 4416 | 154 | 640.0 | 3370 | JPEG:111 |
| Tomato leaf mosaic virus | 130 | 449.5 | 3648 | 69 | 366.5 | 2736 | JPEG:54 |
| Tomato leaf yellow virus | 115 | 638.0 | 4320 | 159 | 505.5 | 3405 | JPEG:76 |
| Tomato mold leaf | 115 | 800.0 | 6000 | 85 | 600.0 | 6000 | JPEG:91 |
| Tomato two spotted spider mites leaf | 960 | 960.0 | 960 | 720 | 720.0 | 720 | JPEG:2 |

*Tableau 3 - Dimensions et formats par classe.*

## Qualité et uniformité du fond
| class_origin | lum_med | contraste_med | flou_lapvar_med | fond_border_std_med |
|---|---|---|---|---|
| Tomato Early blight leaf | 112.76 | 49.92 | 2085.37 | 47.37 |
| Tomato Septoria leaf spot | 118.63 | 46.44 | 2065.21 | 44.71 |
| Tomato leaf | 128.38 | 48.47 | 2127.25 | 40.7 |
| Tomato leaf bacterial spot | 122.28 | 47.84 | 2010.78 | 48.42 |
| Tomato leaf late blight | 114.14 | 47.83 | 1518.13 | 44.83 |
| Tomato leaf mosaic virus | 121.14 | 46.45 | 2152.6 | 50.3 |
| Tomato leaf yellow virus | 117.45 | 46.76 | 3833.68 | 43.88 |
| Tomato mold leaf | 117.85 | 47.11 | 1385.2 | 44.24 |
| Tomato two spotted spider mites leaf | 117.12 | 51.85 | 4830.49 | 51.0 |

*Tableau 4 - Médianes par classe (luminance, contraste, flou, border_std).*

## Correspondances à valider
| class_origin | class_retained | status |
|---|---|---|

*Tableau 5 - Classes dont le statut n'est pas encore CONFIRME.*
