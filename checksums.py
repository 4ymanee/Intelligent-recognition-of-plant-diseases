#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
checksums.py - Empreintes SHA-256 des artefacts 

Génère et vérifie les empreintes des fichiers de preuve (manifestes, rapports, configurations,
partitions, scripts, code des notebooks) SANS les images des corpus, et contrôle que les corpus
clonés sont bien aux révisions attendues.

Commandes (à lancer depuis la racine du dépôt) :
    python checksums.py generate     # écrit CHECKSUMS.sha256
    python checksums.py verify       # compare l'état actuel à CHECKSUMS.sha256
    python checksums.py datasets     # vérifie révisions et effectifs des corpus (DATA_REVISIONS.json)
    python checksums.py all          # verify + datasets

Normalisation (pour que l'empreinte ne dépende ni du système, ni de la date d'exécution) :
  - fins de ligne converties en LF ;
  - JSON : champs volatils (dates, versions, plateforme, commit) ignorés, clés triées ;
  - Markdown : lignes « Généré le ... » et « Décision validée ... » ignorées ;
  - Notebook (.ipynb) : seul le code des cellules est haché (pas les sorties).
Le fichier CHECKSUMS.sha256 n'est donc PAS lisible par `sha256sum -c` : utilisez ce script.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
CHECKSUM_FILE = "CHECKSUMS.sha256"
DATA_FILE = "DATA_REVISIONS.json"

SCOPE_GLOBS = [
    "README.md", "requirements.txt", "DATA_REVISIONS.json", ".gitignore",
    "*.py", "scripts/*.py", "*.ipynb",
    "audit/**/*.csv", "audit/**/*.json", "audit/**/*.md",
    "partitions/**/*.csv", "partitions/**/*.json", "partitions/**/*.md",
    "contamination/**/*.csv", "contamination/**/*.json",
    "conditions_s2/**/*.csv", "conditions_s2/**/*.json", "conditions_s2/**/*.md",
    "runs/**/*.csv", "runs/**/*.json", "runs/**/*.md", "runs/**/*.yaml", "runs/**/*.yml",
    "runs/**/*.keras", "runs/**/*.h5",
]
EXCLUDED_DIRS = {".git", ".venv", "venv", "__pycache__", ".ipynb_checkpoints", "node_modules",
                 "PlantVillage-Dataset", "PlantDoc-Dataset", "review", "paires", "paires_entre_partitions"}
VOLATILE_JSON_KEYS = {"date_utc", "platform", "versions", "git_commit", "date"}
VOLATILE_MD = re.compile(r"^\*?(Généré le|Décision validée)")
IMG_EXT = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def normalize_bytes(path: Path) -> bytes:
    suffix = path.suffix.lower()
    raw = path.read_bytes()
    if suffix in {".keras", ".h5"}:
        return raw
    if suffix == ".ipynb":
        nb = json.loads(raw.decode("utf-8"))
        code = ["".join(c.get("source", "")) for c in nb.get("cells", []) if c.get("cell_type") == "code"]
        return json.dumps(code, ensure_ascii=False).replace("\r\n", "\n").encode("utf-8")
    if suffix == ".json":
        def strip(o):
            if isinstance(o, dict):
                return {k: strip(v) for k, v in o.items() if k not in VOLATILE_JSON_KEYS}
            if isinstance(o, list):
                return [strip(v) for v in o]
            return o
        return json.dumps(strip(json.loads(raw.decode("utf-8"))), sort_keys=True, ensure_ascii=False).encode("utf-8")
    text = raw.decode("utf-8", errors="replace").replace("\r\n", "\n")
    if suffix == ".md":
        text = "\n".join(line for line in text.split("\n") if not VOLATILE_MD.match(line))
    return text.encode("utf-8")


def digest(path: Path) -> str:
    return hashlib.sha256(normalize_bytes(path)).hexdigest()


def in_scope_files() -> list[Path]:
    found: set[Path] = set()
    for pattern in SCOPE_GLOBS:
        for p in ROOT.glob(pattern):
            if p.is_file() and not (set(p.relative_to(ROOT).parts[:-1]) & EXCLUDED_DIRS) and p.suffix.lower() not in IMG_EXT:
                found.add(p)
    return sorted(found, key=lambda p: p.relative_to(ROOT).as_posix())


def cmd_generate() -> int:
    files = in_scope_files()
    lines = [f"{digest(p)}  {p.relative_to(ROOT).as_posix()}" for p in files if p.name != CHECKSUM_FILE]
    (ROOT / CHECKSUM_FILE).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(lines)} empreinte(s) écrites dans {CHECKSUM_FILE}")
    return 0


def cmd_verify(strict: bool = False) -> int:
    cs = ROOT / CHECKSUM_FILE
    if not cs.exists():
        print(f"{CHECKSUM_FILE} introuvable : lancez d'abord `python checksums.py generate`.")
        return 2
    expected = {}
    for line in cs.read_text(encoding="utf-8").splitlines():
        if line.strip():
            h, name = line.split("  ", 1)
            expected[name] = h
    bad = 0
    for name, h in expected.items():
        p = ROOT / name
        if not p.exists():
            print(f"MANQUANT  {name}")
            bad += 1
        elif digest(p) != h:
            print(f"MODIFIÉ   {name}")
            bad += 1
        else:
            print(f"OK        {name}")
    current = {p.relative_to(ROOT).as_posix() for p in in_scope_files() if p.name != CHECKSUM_FILE}
    new = sorted(current - set(expected))
    for name in new:
        print(f"NOUVEAU   {name}  (absent de {CHECKSUM_FILE})")
    ok = len(expected) - bad
    print(f"\nBilan : {ok}/{len(expected)} fichier(s) conformes, {bad} écart(s), {len(new)} nouveau(x).")
    return 1 if bad or (strict and new) else 0


def git_head(repo: Path) -> str:
    try:
        return subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True,
                                       stderr=subprocess.DEVNULL).strip()
    except Exception:
        return ""


def count_images(base: Path, splits: list[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for s in splits:
        d = base / s if s else base
        if not d.exists():
            continue
        for cls in sorted(x for x in d.iterdir() if x.is_dir()):
            n = sum(1 for f in cls.iterdir() if f.is_file() and f.suffix.lower() in IMG_EXT)
            counts[cls.name] = counts.get(cls.name, 0) + n
    return counts


def cmd_datasets() -> int:
    path = ROOT / DATA_FILE
    if not path.exists():
        print(f"{DATA_FILE} introuvable.")
        return 2
    info = json.loads(path.read_text(encoding="utf-8"))
    bad = 0
    for key, d in info.items():
        repo = ROOT / d["path"]
        print(f"\n== {key} ({d['path']}) ==")
        if not repo.exists():
            print("MANQUANT  dossier du corpus absent (voir README, étape 1).")
            bad += 1
            continue
        head = git_head(repo)
        if head == d["commit"]:
            print(f"OK        révision {head[:12]}")
        else:
            print(f"ÉCART     révision {head[:12] or 'inconnue'} (attendue {d['commit'][:12]})")
            bad += 1
        counts = count_images(repo / d["images_root"], d.get("splits", [""]))
        for cls, exp in d["expected_counts"].items():
            got = counts.get(cls, 0)
            tag = "OK       " if got == exp else "ÉCART    "
            bad += 0 if got == exp else 1
            print(f"{tag} {cls}: {got} image(s) (attendu {exp})")
        extra = sorted(set(counts) - set(d["expected_counts"]))
        if extra:
            print(f"INFO      dossiers non listés : {', '.join(extra)}")
    print(f"\nBilan corpus : {bad} écart(s).")
    return 1 if bad else 0


def main() -> None:
    ap = argparse.ArgumentParser(description="Empreintes SHA-256 des artefacts du PFA 07.")
    ap.add_argument("command", choices=["generate", "verify", "datasets", "all"])
    ap.add_argument("--strict", action="store_true", help="verify : un fichier nouveau est aussi une erreur")
    args = ap.parse_args()
    if args.command == "generate":
        code = cmd_generate()
    elif args.command == "verify":
        code = cmd_verify(args.strict)
    elif args.command == "datasets":
        code = cmd_datasets()
    else:
        code = max(cmd_verify(args.strict), cmd_datasets())
    sys.exit(code)


if __name__ == "__main__":
    main()
