from pathlib import Path
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Customer Intelligence – Retail", page_icon="🛍️", layout="wide")
st.title("🛍️ Customer Intelligence – E-commerce")
st.caption("Analyse des ventes, des clients, des produits et des marchés | Atelier pédagogique")

DATA = Path(__file__).parent / "data" / "online_retail.csv"

@st.cache_data
def load_data(path):
    df = pd.read_csv(path, encoding="latin1")
    required = ["InvoiceNo","StockCode","Description","Quantity","InvoiceDate","UnitPrice","CustomerID","Country"]
    missing = set(required) - set(df.columns)
    if missing:
        raise ValueError(f"Colonnes manquantes : {sorted(missing)}")
    df["InvoiceNo"] = df["InvoiceNo"].astype("string").str.strip()
    df["StockCode"] = df["StockCode"].astype("string").str.strip()
    df["Country"] = df["Country"].astype("string").str.strip()
    df["Description"] = df["Description"].astype("string").str.strip()
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], format="%m/%d/%Y %H:%M", errors="coerce")
    df["CustomerID"] = pd.to_numeric(df["CustomerID"], errors="coerce").astype("Int64")
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")
    df["LineRevenue"] = df["Quantity"] * df["UnitPrice"]
    df["IsCancellation"] = df["InvoiceNo"].str.startswith("C", na=False)
    df["YearMonth"] = df["InvoiceDate"].dt.to_period("M").dt.to_timestamp()
    return df

try:
    raw = load_data(DATA)
except Exception as e:
    st.error(f"Impossible de charger le fichier : {e}")
    st.stop()

st.sidebar.header("Filtres")
countries = sorted(raw["Country"].dropna().unique().tolist())
selected_countries = st.sidebar.multiselect("Pays", countries, default=["United Kingdom"] if "United Kingdom" in countries else countries)
min_d, max_d = raw["InvoiceDate"].min().date(), raw["InvoiceDate"].max().date()
date_range = st.sidebar.date_input("Période", value=(min_d, max_d), min_value=min_d, max_value=max_d)
include_unknown = st.sidebar.checkbox("Inclure les transactions sans CustomerID dans les ventes", value=True)

df = raw[raw["Country"].isin(selected_countries)].copy()
if isinstance(date_range, (tuple,list)) and len(date_range)==2:
    df = df[df["InvoiceDate"].dt.date.between(date_range[0], date_range[1])]

# Business rule: sales KPIs use positive quantities/prices and non-cancellation invoices.
# Negative quantities and cancellation invoices are retained for separate returns/cancellation analysis.
sales = df[(~df["IsCancellation"]) & (df["Quantity"] > 0) & (df["UnitPrice"] > 0)].copy()
if not include_unknown:
    sales = sales[sales["CustomerID"].notna()]
returns = df[(df["Quantity"] < 0) | df["IsCancellation"]].copy()

st.caption(f"Périmètre filtré : {len(df):,} lignes | Ventes retenues : {len(sales):,} lignes".replace(",", " "))
revenue = sales["LineRevenue"].sum()
orders = sales["InvoiceNo"].nunique()
customers = sales["CustomerID"].nunique()
units = sales["Quantity"].sum()
a,b,c,d,e=st.columns(5)
a.metric("CA brut des lignes retenues", f"{revenue:,.0f} £".replace(",", " "))
b.metric("Commandes", f"{orders:,}".replace(",", " "))
c.metric("Clients identifiés", f"{customers:,}".replace(",", " "))
d.metric("Unités vendues", f"{units:,.0f}".replace(",", " "))
e.metric("Panier moyen / commande", f"{revenue/orders:,.2f} £" if orders else "—")

st.info("Définition pédagogique : le CA affiché est la somme Quantity × UnitPrice des lignes positives, hors factures d'annulation et prix non positifs. Il s'agit d'un CA brut calculé sur les lignes, pas d'une marge ni d'un bénéfice. Les retours sont analysés séparément.")

tab1,tab2,tab3,tab4=st.tabs(["Vue d'ensemble","Clients","Produits","Qualité & méthode"])

with tab1:
    st.subheader("Évolution des ventes")
    monthly=sales.groupby("YearMonth",as_index=False).agg(CA=("LineRevenue","sum"),Commandes=("InvoiceNo","nunique"))
    fig=px.line(monthly,x="YearMonth",y="CA",markers=True,title="Chiffre d'affaires mensuel (£)")
    st.plotly_chart(fig,use_container_width=True)
    left,right=st.columns(2)
    with left:
        by_country=sales.groupby("Country",as_index=False).agg(CA=("LineRevenue","sum")).sort_values("CA",ascending=False).head(10)
        st.plotly_chart(px.bar(by_country.sort_values("CA"),x="CA",y="Country",orientation="h",title="Top 10 pays par CA"),use_container_width=True)
    with right:
        sales["Weekday"] = sales["InvoiceDate"].dt.day_name()
        weekday_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        daily=sales.groupby("Weekday",as_index=False).agg(CA=("LineRevenue","sum"))
        daily["Weekday"] = pd.Categorical(daily["Weekday"], categories=weekday_order, ordered=True)
        daily=daily.sort_values("Weekday")
        st.plotly_chart(px.bar(daily,x="Weekday",y="CA",title="CA par jour de la semaine"),use_container_width=True)

with tab2:
    st.subheader("Segmentation et valeur client")
    identified=sales.dropna(subset=["CustomerID"]).copy()
    cust=(identified.groupby("CustomerID",as_index=False)
          .agg(CA=("LineRevenue","sum"),Commandes=("InvoiceNo","nunique"),
               DernierAchat=("InvoiceDate","max"),Unites=("Quantity","sum")))
    if not cust.empty:
        ref_date=identified["InvoiceDate"].max()+pd.Timedelta(days=1)
        cust["Recence_jours"]=(ref_date-cust["DernierAchat"]).dt.days
        cust["Frequence"]=cust["Commandes"]
        cust["Monetaire"]=cust["CA"]
        q_r=cust["Recence_jours"].quantile([.25,.5,.75]).to_dict()
        q_f=cust["Frequence"].quantile([.25,.5,.75]).to_dict()
        q_m=cust["Monetaire"].quantile([.25,.5,.75]).to_dict()
        st.dataframe(cust.sort_values("CA",ascending=False).head(20),use_container_width=True,hide_index=True)
        l,r=st.columns(2)
        with l:
            st.plotly_chart(px.histogram(cust,x="CA",nbins=40,title="Distribution du CA par client"),use_container_width=True)
        with r:
            st.plotly_chart(px.scatter(cust,x="Commandes",y="CA",hover_data=["CustomerID"],title="Fréquence d'achat vs CA client"),use_container_width=True)
        st.caption("RFM exploratoire : Récence = jours depuis le dernier achat ; Fréquence = nombre de factures ; Montant = CA cumulé. Les seuils et règles de scoring doivent être explicités avant toute activation marketing.")
    else:
        st.warning("Aucun client identifié dans le périmètre sélectionné.")

with tab3:
    st.subheader("Performance des produits")
    prod=sales.groupby(["StockCode","Description"],dropna=False,as_index=False).agg(
        CA=("LineRevenue","sum"),Quantite=("Quantity","sum"),Commandes=("InvoiceNo","nunique"))
    top=prod.sort_values("CA",ascending=False).head(15)
    st.plotly_chart(px.bar(top.sort_values("CA"),x="CA",y="Description",orientation="h",title="Top 15 produits par CA"),use_container_width=True)
    st.dataframe(top,use_container_width=True,hide_index=True)

with tab4:
    st.subheader("Contrôle qualité")
    q1,q2,q3,q4=st.columns(4)
    q1.metric("Lignes source",f"{len(raw):,}".replace(",", " "))
    q2.metric("Doublons exacts",f"{raw.duplicated().sum():,}".replace(",", " "))
    q3.metric("CustomerID manquant",f"{raw['CustomerID'].isna().sum():,}".replace(",", " "))
    q4.metric("Descriptions manquantes",f"{raw['Description'].isna().sum():,}".replace(",", " "))
    quality=pd.DataFrame({
        "Contrôle":["Quantité négative","Prix nul ou négatif","Facture d'annulation (préfixe C)","Date invalide"],
        "Nombre":[int((raw["Quantity"]<0).sum()),int((raw["UnitPrice"]<=0).sum()),int(raw["InvoiceNo"].str.startswith("C",na=False).sum()),int(raw["InvoiceDate"].isna().sum())]
    })
    st.dataframe(quality,use_container_width=True,hide_index=True)
    st.markdown("""
    **Règles à discuter et documenter**
    - Ne pas supprimer automatiquement les doublons : vérifier leur nature et l'impact métier.
    - Les quantités négatives et les factures préfixées par `C` peuvent représenter retours/annulations.
    - Les clients sans `CustomerID` restent comptés dans les ventes agrégées si l'option correspondante est cochée, mais ne peuvent pas entrer dans une segmentation individuelle.
    - Le CA calculé n'intègre ni coût d'achat, ni frais, ni marge, ni coûts marketing.
    """)

st.divider()
st.subheader("Export des agrégats")
csv=sales.groupby("Country",as_index=False).agg(CA=("LineRevenue","sum"),Commandes=("InvoiceNo","nunique")).to_csv(index=False).encode("utf-8")
st.download_button("Télécharger la synthèse par pays (CSV)",csv,"synthese_pays.csv","text/csv")
