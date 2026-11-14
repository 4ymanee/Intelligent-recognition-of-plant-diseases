#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
restore_invalid_names.py - Restaure les fichiers d'un dépôt git dont le nom contient
des caractères interdits sous Windows (ex. '?' dans PlantDoc), en les écrivant sous un
nom assaini. Chaque restauration est consignée (chemin d'origine -> chemin restauré,
SHA-256) pour garder la traçabilité de l'audit.

Usage (depuis n'importe où, sous Windows) :
    python restore_invalid_names.py --repo PlantDoc-Dataset --log audit/pd/restored_files.csv

Options :
    --prefix  préfixes de chemins à traiter (défaut : train/Tomato test/Tomato)
    --all-missing restaure AUSSI les fichiers à nom valide absents du disque (cas où
              git checkout s'est interrompu sur les erreurs 'invalid path')
    --dry-run liste ce qui serait restauré sans rien écrire

Règle d'assainissement : chaque caractère parmi  < > : " \\ | ? *  (et les caractères de
contrôle) est remplacé par '_'. En cas de collision de noms, un suffixe court dérivé du
chemin d'origine est ajouté. Le script est idempotent (relançable sans effet de bord).
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import re
import subprocess
import sys
from pathlib import Path

INVALID = re.compile(r'[<>:"\\|?*\x00-\x1f]')


def sanitize_component(c: str) -> str:
    return INVALID.sub("_", c).rstrip(" .") or "_"


def run_git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True)


def main() -> None:
    ap = argparse.ArgumentParser(description="Restaure les fichiers aux noms invalides sous Windows.")
    ap.add_argument("--repo", type=Path, default=Path("."), help="dossier du dépôt git cloné")
    ap.add_argument("--prefix", nargs="+", default=["train/Tomato", "test/Tomato"],
                    help="préfixes de chemins à traiter")
    ap.add_argument("--log", type=Path, default=Path("restored_files.csv"))
    ap.add_argument("--all-missing", action="store_true",
                    help="restaurer aussi les fichiers à nom valide absents du disque")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    r = run_git(args.repo, "ls-tree", "-r", "-z", "--name-only", "HEAD")
    if r.returncode != 0:
        sys.exit("git ls-tree a échoué : " + r.stderr.decode(errors="replace"))
    paths = sorted(p for p in r.stdout.decode("utf-8", errors="replace").split("\0") if p)

    assigned: dict[str, str] = {}
    rows = []
    for p in paths:
        if not any(p.startswith(x) for x in args.prefix):
            continue
        comps = p.split("/")
        clean = [sanitize_component(c) for c in comps]
        valid_name = clean == comps
        if valid_name and (not args.all_missing or (args.repo / Path(*comps)).exists()):
            continue  # nom valide et déjà présent : géré par git checkout
        dest_rel = "/".join(clean)
        if dest_rel in assigned and assigned[dest_rel] != p:  # collision
            stem, dot, ext = clean[-1].rpartition(".")
            tag = hashlib.sha1(p.encode("utf-8")).hexdigest()[:6]
            clean[-1] = f"{stem}_{tag}.{ext}" if dot else f"{clean[-1]}_{tag}"
            dest_rel = "/".join(clean)
        assigned[dest_rel] = p
        dest = args.repo / Path(*clean)
        kind = "nom_valide_manquant" if valid_name else "nom_invalide"

        status, sha, size = "a_restaurer", "", ""
        if dest.exists():
            status = "deja_present"
            sha = hashlib.sha256(dest.read_bytes()).hexdigest()
            size = dest.stat().st_size
        elif not args.dry_run:
            blob = run_git(args.repo, "cat-file", "blob", f"HEAD:{p}")
            if blob.returncode != 0:
                status = "echec"
            else:
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(blob.stdout)
                status = "restaure"
                sha = hashlib.sha256(blob.stdout).hexdigest()
                size = len(blob.stdout)
        rows.append({"chemin_origine_depot": p, "chemin_restaure": dest_rel, "type": kind,
                     "statut": status, "sha256": sha, "taille_octets": size})

    if not args.dry_run:
        args.log.parent.mkdir(parents=True, exist_ok=True)
        with args.log.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["chemin_origine_depot", "chemin_restaure", "type",
                                              "statut", "sha256", "taille_octets"])
            w.writeheader()
            w.writerows(rows)

    counts: dict[str, int] = {}
    for row in rows:
        counts[row["statut"]] = counts.get(row["statut"], 0) + 1
    print(f"{len(rows)} fichier(s) traités sous {args.prefix} : {counts}")
    if not args.dry_run:
        print(f"Journal écrit dans {args.log}")


if __name__ == "__main__":
    main()