"""Extraction BPE pour les communes d'un departement, avec libelles."""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import melodi

DEP = "79"
OUT = pathlib.Path(__file__).resolve().parent.parent / "outputs"

if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)

    ref = melodi.get_range()
    df = melodi.get_data({"GEO": f"DEP-{DEP}*COM"})

    # GEO s'ecrit millesime-niveau-code, comme dans le package R de l'Insee
    df[["GEO_REF", "GEO_OBJECT", "CODE_COMMUNE"]] = df["GEO"].str.split("-", expand=True)

    for col in ["FACILITY_DOM", "FACILITY_SDOM", "FACILITY_TYPE"]:
        df = melodi.libeller(df, ref, col)

    ref.to_csv(OUT / "dictionnaire_dimensions.csv", index=False, encoding="utf-8")
    df.to_csv(OUT / f"bpe_{DEP}_communes_complet.csv", index=False, encoding="utf-8")

    total = df[(df["FACILITY_DOM"] == "_T") & (df["FACILITY_TYPE"] == "_T")]
    total = total[["CODE_COMMUNE", "OBS_VALUE_NIVEAU"]]
    total = total.rename(columns={"OBS_VALUE_NIVEAU": "NB_EQUIPEMENTS"})
    total = total.sort_values("NB_EQUIPEMENTS", ascending=False)
    total.to_csv(OUT / f"bpe_{DEP}_total_par_commune.csv", index=False, encoding="utf-8")

    dom = df[(df["FACILITY_SDOM"] == "_T") & (df["FACILITY_DOM"] != "_T")]
    dom = dom.groupby("FACILITY_DOM_LABEL", as_index=False)["OBS_VALUE_NIVEAU"].sum()
    dom = dom.rename(columns={"FACILITY_DOM_LABEL": "DOMAINE",
                              "OBS_VALUE_NIVEAU": "NB_EQUIPEMENTS"})
    dom = dom.sort_values("NB_EQUIPEMENTS", ascending=False)
    dom.to_csv(OUT / f"bpe_{DEP}_par_domaine.csv", index=False, encoding="utf-8")

    print("Millesime :", sorted(df["TIME_PERIOD"].unique()))
    print("Lignes :", len(df))
    print("Communes :", total["CODE_COMMUNE"].nunique())
    print()
    print(dom.to_string(index=False))
