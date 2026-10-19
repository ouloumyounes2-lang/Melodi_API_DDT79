"""Fonctions d'appel a l'API Melodi de l'Insee (jeu DS_BPE)."""

import requests
import pandas as pd

BASE = "https://api.insee.fr/melodi"
DS = "DS_BPE"
MAX_RESULT = 100000


def compter(filtres):
    params = dict(filtres, totalCount="true", maxResult=0)
    r = requests.get(f"{BASE}/data/{DS}", params=params, timeout=60)
    r.raise_for_status()
    return r.json()["paging"]["count"]


def get_data(filtres):
    n = compter(filtres)
    if n == 0:
        raise ValueError(f"Aucun resultat pour {filtres}")
    if n > MAX_RESULT:
        raise ValueError(f"{n} lignes, au-dela du maximum de {MAX_RESULT}")

    params = dict(filtres, maxResult=MAX_RESULT)
    r = requests.get(f"{BASE}/data/{DS}", params=params, timeout=300)
    r.raise_for_status()

    lignes = []
    for o in r.json()["observations"]:
        ligne = {}
        ligne.update(o.get("dimensions") or {})
        ligne.update(o.get("attributes") or {})
        for nom, val in (o.get("measures") or {}).items():
            ligne[nom] = val.get("value") if isinstance(val, dict) else val
        lignes.append(ligne)
    return pd.DataFrame(lignes)


def get_range(lang="fr", exclure=("GEO",)):
    r = requests.get(f"{BASE}/range/{DS}", timeout=120)
    r.raise_for_status()
    lignes = []
    for dim in r.json()["range"]:
        code_dim = dim["concept"]["code"]
        if code_dim in exclure:
            continue
        lib_dim = (dim["concept"].get("label") or {}).get(lang)
        for v in dim.get("values", []):
            lignes.append({
                "DIM": code_dim,
                "DIM_LABEL": lib_dim,
                "MOD": v["code"],
                "MOD_LABEL": (v.get("label") or {}).get(lang),
            })
    return pd.DataFrame(lignes)


def libeller(df, ref, colonne):
    corr = ref[ref["DIM"] == colonne][["MOD", "MOD_LABEL"]]
    corr = corr.rename(columns={"MOD": colonne, "MOD_LABEL": colonne + "_LABEL"})
    return df.merge(corr, on=colonne, how="left")
