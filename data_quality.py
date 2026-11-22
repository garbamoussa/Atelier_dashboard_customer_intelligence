import pandas as pd

def audit(df: pd.DataFrame) -> dict:
    """Diagnostic non destructif : ne supprime aucune ligne."""
    return {
        "lignes": int(len(df)),
        "doublons_exacts": int(df.duplicated().sum()),
        "valeurs_manquantes": df.isna().sum().to_dict(),
        "quantites_negatives": int((df["Quantity"] < 0).sum()),
        "prix_nuls_ou_negatifs": int((df["UnitPrice"] <= 0).sum()),
        "factures_annulees": int(df["InvoiceNo"].astype(str).str.startswith("C").sum()),
    }

def add_business_fields(df: pd.DataFrame) -> pd.DataFrame:
    """Ajoute des champs calculés sans écraser les colonnes source."""
    out = df.copy()
    out["LineRevenue"] = out["Quantity"] * out["UnitPrice"]
    out["IsCancellation"] = out["InvoiceNo"].astype(str).str.startswith("C")
    out["InvoiceDate"] = pd.to_datetime(out["InvoiceDate"], format="%m/%d/%Y %H:%M", errors="coerce")
    return out
