# Rapport de partition - PlantVillage (tomate)

*Généré le 2026-11-08T13:01:36+00:00 UTC - graine 42 - empreinte du manifeste `2b3bbacc616c75f9...` - empreinte de leaf-map `3b4b253683c69117...`*

## Synthèse
- Images éligibles : **7209** ; partitionnées (feuille identifiée) : **4870** ; réserve non cartographiée : **2339**.
- Groupes (feuilles après fusion) : **1218**.
- Contrôles anti-fuite : **tous réussis** (feuilles, groupes, clusters de quasi-doublons, SHA-256).

## Couverture de leaf-map.json
| class_retained | n_images | cartographiees | non_cartographiees | taux_couverture_% |
|---|---|---|---|---|
| alternariose_precoce | 1000 | 999 | 1 | 99.9 |
| cladosporiose | 952 | 952 | 0 | 100.0 |
| mildiou_tardif | 1901 | 920 | 981 | 48.4 |
| saine | 1585 | 999 | 586 | 63.0 |
| septoriose | 1771 | 1000 | 771 | 56.5 |

*Tableau 1 - Couverture du regroupement par feuille, par classe.*

## Images par classe et par partition
| class_retained | train | val | test | total |
|---|---|---|---|---|
| alternariose_precoce | 703 | 148 | 148 | 999 |
| cladosporiose | 668 | 144 | 140 | 952 |
| mildiou_tardif | 644 | 140 | 136 | 920 |
| saine | 703 | 148 | 148 | 999 |
| septoriose | 700 | 152 | 148 | 1000 |

*Tableau 2 - Effectifs (images).*

| class_retained | train | val | test |
|---|---|---|---|
| alternariose_precoce | 70.4 | 14.8 | 14.8 |
| cladosporiose | 70.2 | 15.1 | 14.7 |
| mildiou_tardif | 70.0 | 15.2 | 14.8 |
| saine | 70.4 | 14.8 | 14.8 |
| septoriose | 70.0 | 15.2 | 14.8 |

*Tableau 3 - Proportions (%) par classe.*

| primary_class | train | val | test |
|---|---|---|---|
| alternariose_precoce | 176 | 37 | 37 |
| cladosporiose | 167 | 36 | 35 |
| mildiou_tardif | 161 | 35 | 34 |
| saine | 176 | 37 | 37 |
| septoriose | 175 | 38 | 37 |

*Tableau 4 - Nombre de groupes (feuilles) par partition.*

## Sources d'acquisition par classe (sous-ensemble partitionné)
| class_retained | crnl_l.mold | matt.s_cg | rs_erly.b | rs_hl | rs_late.b |
|---|---|---|---|---|---|
| alternariose_precoce | 0 | 0 | 999 | 0 | 0 |
| cladosporiose | 952 | 0 | 0 | 0 | 0 |
| mildiou_tardif | 0 | 0 | 0 | 0 | 920 |
| saine | 0 | 0 | 0 | 999 | 0 |
| septoriose | 0 | 1000 | 0 | 0 | 0 |

*Tableau 5 - Nombre d'images par source et par classe.*

## Règle appliquée
Les partitions sont définies au niveau des feuilles (identifiants fournis par les auteurs du corpus) ; les feuilles reliées par un cluster de quasi-doublons ou par un fichier identique sont fusionnées ; les groupes sont répartis de façon stratifiée par classe, avec une graine fixe, avant toute augmentation. Les images sans identifiant de feuille sont mises de côté.
