import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import base64
from io import BytesIO
import pandas as pd
import openpyxl
import os 
import numpy as np
from pathlib import Path
import plotly.express as px

#📁 Chemins des fichiers
base_dir = Path(__file__).parent.resolve()
df2_path = base_dir / "Fichiers" / "LBE_Anonyme.xlsx"
df1_path = base_dir / "Fichiers" / "VOLTERRES_Anonyme.xlsx"
df_fusionne_path = base_dir / "Fichiers" / "df_fusionne_Anonyme.csv"

logo_path = base_dir / "Images" / "logo-sivom-sage.png"
image_path = base_dir / "Images" / "stageDATA.png"
miage_path = base_dir / "Images" / "MIAGE.png"



# ✅ Mise en cache des fichiers Excel et csv
@st.cache_data
def load_volterres_data(path):
    return pd.read_excel(path)

@st.cache_data
def load_lbe_data(path):
    return pd.read_excel(path, header=[0, 1])

@st.cache_data
def load_df_fusionne(path):
    return pd.read_csv(path, sep=';')

# ✅ Mettre en cache la conversion d’image en base64 (pour le logo)
@st.cache_data
def image_to_base64(image_path):
    img = Image.open(image_path)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

@st.cache_data
def load_image(path):
    # Charger en bytes pour le cache Streamlit (pas un objet PIL directement)
    with open(path, "rb") as f:
        return f.read()

@st.cache_data
def resize_image(image_bytes, factor):
    # Charger les bytes en image
    img = Image.open(BytesIO(image_bytes))
    new_size = (img.width * factor, img.height * factor)
    img_resized = img.resize(new_size, Image.LANCZOS)

    # Convertir l'image redimensionnée en bytes pour affichage rapide
    buffered = BytesIO()
    img_resized.save(buffered, format="PNG")
    return buffered.getvalue()  # image en bytes


# Chargement logos et images
logo_base64 = image_to_base64(logo_path)
image = load_image(image_path)
miage_logo = load_image(miage_path)


# Redimensionnement de l'image page 1
factor = 2
image_resized_bytes = resize_image(image, factor)  



# === BARRE LATÉRALE ET LISTE DES PAGES  =========================================================================================
st.sidebar.title("Salomé Saintin")
st.sidebar.markdown("**L3 MIASHS parcours-type MIAGE**")
st.sidebar.markdown("12/05/2025 - 01/09/2025")
st.sidebar.markdown("---")  # ligne de séparation

st.sidebar.title("Sommaire")
pages = ["Introduction", "Fichiers bruts", "Transformations réalisées", "Fichier Final", "Statistiques et visualisations", "Conclusion"]
page = st.sidebar.radio("Aller vers", pages)



st.sidebar.markdown("---")  # ligne de séparation
st.sidebar.image(miage_logo , use_container_width=True)



# === TITRE & LOGO =================================================================================================
st.markdown(f"""
    <div style="display: flex; align-items: center;">
        <img src="data:image/png;base64,{logo_base64}" style="height:80px; margin-right: 40px;">
        <h1 style="margin: 0;">STAGE - SPL Les Eaux du SAGe</h1>
    </div>
    """, unsafe_allow_html=True)


# === SOUS-TITRE =====================================================================================================
st.write("***&nbsp;&nbsp; Flux de transformation des factures d'énergie pour créer un tableau de bord de gestion des contrats***")






# === PAGE 1 : Introduction ===========================================================================================
if page == "Introduction":
    st.markdown("""
    <ul style='line-height: 1.5;'>
        <li><strong>Problématique</strong> Les factures des consommations électriques n’avaient pas la même structure selon leur fournisseur (La Belle Énergie ou Volterres) :
nombre de colonnes distinct : 158 pour LBE et 124 pour Volterres
nom de colonnes différent 
formats et types de données hétérogènes. Cette hétérogénéité des données empêchait leur combinaison et leur analyse correcte dans Power BI qui requiert des structures uniformes. 
:</li>
        <li><strong>La source</strong> : Transformer et fusionner les factures des deux fournisseurs : Volterres et Lbe</li>
    </ul>
    """, unsafe_allow_html=True)

    

# === AFFICHER L'IMAGE EN DESSOUS ===================================================================
    st.image(image_resized_bytes, use_container_width=True)


    st.markdown("""
    <h4 style='line-height: 1.2;'>Importance de la qualité des données</h4>
    <ul style='line-height: 1.5;'>
        <li><strong>La démarche : </strong>
            <ul style='line-height: 1.5;'>
                <li> Récupérer les données sources</li>
                <li> Corriger les sources de données qui ne sont pas toujours de bonne qualité</li>
                <li> Harmoniser les colonnes pour pouvoir fusionner les deux fichiers</li>
            </ul>
        </li>
    </ul>
    """, unsafe_allow_html=True)



# === PAGE 2 : Fichiers bruts ===============================================
if page == "Fichiers bruts":
    st.markdown("""
    <ul style='line-height: 1.5;'>
        <li><strong>La source</strong> : Deux fichiers Excel des factures originales issues du téléchargement sur les sites extranet des deux fournisseurs d'électricité. </li>
        <li><strong>La demande</strong> : Créer un flux permettant de charger les factures dans un modèle Power BI. 
            À l'avenir le flux sera automatisé, mais dans le cadre du stage j'ai réalisé un flux en Python pour transformer les fichiers automatiquement à partir des exports Excel mensuels.</li>
     <li><strong>A noter</strong> : Pour des raisons de confidentialité les fichiers ont été anonymisés.</li>
    </ul>
    """, unsafe_allow_html=True)

    try:
        df1 = load_volterres_data(df1_path)
        st.success(f"✅ Données Volterres chargées : {df1.shape}")
    except Exception as e:
        st.error(f"❌ Erreur chargement Volterres : {e}")
        df1 = pd.DataFrame()

    try:
        df2 = load_lbe_data(df2_path)
        st.success(f"✅ Données LBE chargées : {df2.shape}")
    except Exception as e:
        st.error(f"❌ Erreur chargement LBE : {e}")
        df2 = pd.DataFrame()

    if not df1.empty:
        st.subheader("Aperçu des factures Volterres")
        st.dataframe(df1.head(40), height=250)
        st.write("📏 Dimensions du fichier Volterres :", df1.shape)

    if not df2.empty:
        st.subheader("Aperçu des factures LBE")
        max_rows = 10
        df2_preview = df2.head(max_rows)

        st.markdown(f"""
            <div style="overflow-x: auto; overflow-y: auto; border: 1px solid #ddd; padding: 10px; height: 350px;">
            {df2_preview.to_html(index=False)}
            </div>
        """, unsafe_allow_html=True)


        st.write("📏 Dimensions complètes du fichier LBE :", df2.shape)
        st.write("🛠️ Dans le fichier de départ LBE, les entêtes sont sur deux colonnes et les intitulés ne correspondent pas à ceux du fichier Volterres.")
        st.write("🔁 Il est nécessaire de normaliser la saisie des données pour pouvoir les analyser efficacement.")



# === PAGE 3 : Transformations réalisées ===========================================================================================
if page == "Transformations réalisées":
    st.markdown("""
        <style>
        .small-font { font-size: 14px; }
        .medium-font { font-size: 18px; }
        </style>
        <h2>Transformations réalisées</h2>
        <p>Voici un résumé des principales transformations appliquées aux données :</p>
        <ul>
            <li>Renommage des colonnes selon un dictionnaire défini</li>
            <li>Nettoyage des valeurs nulles et suppression des lignes vides</li>
            <li>Création de colonnes calculées (Total_HTVA, Durée de période de consommation, etc.)</li>
            <li>Conversion des formats (dates, types numériques)</li>
            <li>Fusion des données des deux fournisseurs</li>
        </ul>
        """, unsafe_allow_html=True)

    st.markdown('<p class="medium-font"><b>1- Données fournisseur Volterres :</b></p>', unsafe_allow_html=True)

    # ------------------ VOLTERRES ------------------
    
    st.markdown('<p class="small-font"><li>Standardisation des noms de colonnes via un dictionnaire</li></p>', unsafe_allow_html=True)
    with st.expander(""):
        st.code("""
    dico_colonnes1 = {
        "Numéro de PDL": "Numero_PDL",
        "N° de facture": "Numero_facture",
        "Date de facturation": "Date_facture",
        "Date de début de relève": "Date_debut_periode",
        "Date de fin de relève": "Date_fin_periode",
        "Transport et distribution (€HT)": "Tarif_acheminement",
        "Taxes et contributions locales (€HTVA)": "Tarif_taxes_contributions_locales",
        "Électricité et options associées (€HT)": "Tarif_fourniture",
        "Total à payer (€TTC)": "Total_TTC",
        "Total TVA (€)": "Total_TVA",
        "Segment": "Segment",
        "Numéro de contrat": "Numero_contrat",
        "Formule Tarifaire d'Acheminement": "Formule_tarifaire_acheminement",
        "Puissance souscrite": "Puissance_souscrite",
        'Consommation Heures pleines saison haute (kWh)': "Consommation_HPH",
        'Consommation Heures creuses saison haute (kWh)': "Consommation_HCH",
        'Consommation Heures pleines saison basse (kWh)': "Consommation_HPB",
        'Consommation Heures creuses saison basse (kWh)': "Consommation_HCB",
        'Consommation Base (kWh)': "Consommation_BASE",
        'Consommation Heures pleines (kWh)': "Consommation_HP",
        'Consommation Heures creuses (kWh)': "Consommation_HC",
        'Consommation Pointe (kWh)': "Consommation_POINTE",
        'Consommation totale (kWh)': "Consommation_totale",
        'dont CEE (€HT)': "CEE",
        'dont Capacité (€HT)': "Capacite",
        "dont Garanties d'origine (€HT)": "Garantie_origine",
        'CTA (€HTVA)': "CTA",
        'CSPE (€HTVA)': "CSPE",
        'dont Dépassement de puissance (€HT)': "Depassement",
        'Dépassement de puissance souscrite (h ou kWh)': "Depassement_puissance_souscrite",
        'Prestations GRD (€HT)': "Prestations_GRD",
        'Frais et remises (€HT)': "Frais_remises_supplementaires",
        'Adresse': "Adresse_facture",
        'Code postal': "CP_facture",
        'Ville': "Ville_facture"
    }
        df_renomme1 = df1.rename(columns=dico_colonnes1)[[col for col in dico_colonnes1.values() if col in df1.rename(columns=dico_colonnes1).columns]].copy()
                """, language="python")

    
    st.markdown('<p class="small-font"><li>Nettoyage des lignes vides</li></p>', unsafe_allow_html=True)
    with st.expander(""):
            
        st.code("""
    df_renomme1 = df_renomme1.dropna(how='all')
    df_renomme1.replace(r'^\\s*$', np.nan, regex=True, inplace=True)
    df_renomme1.replace(['nan', 'NaN', 'None'], np.nan, inplace=True)
                """, language="python")
        
    st.markdown('<p class="small-font"><li>Création de colonnes calculées et colonnes imposées</li></p>', unsafe_allow_html=True)
    with st.expander(""):
            
        st.code("""
    df_renomme1["Total_HTVA"] = (
        df_renomme1["Tarif_acheminement"] +
        df_renomme1["Tarif_taxes_contributions_locales"] +
        df_renomme1["Tarif_fourniture"] +
        df_renomme1["Prestations_GRD"] +
        df_renomme1["Frais_remises_supplementaires"]
    )

    df_renomme1["Duree_periode_consommation"] = (
        df_renomme1["Date_fin_periode"] - df_renomme1["Date_debut_periode"]
    ).dt.days

    df_renomme1["Nom_fournisseur"] = "Volterres"
    df_renomme1["Client_final"] = "SPL LES EAUX DU SAGE"
                """, language="python")

    
    st.markdown('<p class="small-font"><li>Normalisation des formats</li></p>', unsafe_allow_html=True)
    with st.expander(""):
        st.code("""
   
    #Colonnes texte en string
df_renomme1["Numero_PDL"] = df_renomme1["Numero_PDL"].astype("string").str.strip().str.replace(r"\.0$", "", regex=True)
df_renomme1["Adresse_facture"] = df_renomme1["Adresse_facture"].astype("string").str.strip().str.replace(r"\.0$", "", regex=True)
df_renomme1['CP_facture'] = df_renomme1['CP_facture'].astype("string").str.strip().str.replace(r"\.0$", "", regex=True)
df_renomme1['Ville_facture'] = df_renomme1['Ville_facture'].astype("string").str.strip().str.replace(r"\.0$", "", regex=True)
df_renomme1["Numero_facture"] = df_renomme1["Numero_facture"].astype("string").str.strip().str.replace(r"\.0$", "", regex=True)
df_renomme1["Numero_contrat"] = df_renomme1["Numero_contrat"].astype("string").str.strip().str.replace(r"\.0$", "", regex=True)
df_renomme1["Formule_tarifaire_acheminement"] = df_renomme1["Formule_tarifaire_acheminement"].astype("string").str.strip().str.replace(r"\.0$", "", regex=True)
df_renomme1["Nom_fournisseur"] = df_renomme1["Nom_fournisseur"].astype("string").str.strip().str.replace(r"\.0$", "", regex=True)
df_renomme1["Puissance_souscrite"] = df_renomme1["Puissance_souscrite"].astype("string").str.strip().str.replace(r"\.0$", "", regex=True)
df_renomme1["Client_final"] = df_renomme1["Client_final"].astype("string").str.strip().str.replace(r"\.0$", "", regex=True)

    #Colonnes numériques en float
df_renomme1[[
    "Consommation_HPH", "Garantie_origine", "Capacite", "CEE",
    "Consommation_totale", "Consommation_HCB", "Consommation_HPB", "Consommation_HCH"
]] = df_renomme1[[
    "Consommation_HPH", "Garantie_origine", "Capacite", "CEE",
    "Consommation_totale", "Consommation_HCB", "Consommation_HPB", "Consommation_HCH"
]].astype(float) 
                """, language="python")

# ------------------ LBE ------------------

    st.markdown('<p class="small-font"><b>2. Données fournisseur LBE</b></p>', unsafe_allow_html=True) 

    st.markdown('<p class="small-font"><li>Fusion des deux lignes d\'entêtes et nettoyage des textes</li></p>', unsafe_allow_html=True)
    with st.expander(""):

        st.code("""
    df2 = pd.read_excel(df2_path, header=[0, 1])

    def clean_col(col):
        if isinstance(col, tuple):
            col = " ".join([str(c) for c in col if c])
        s = str(col).strip()
        s = s.replace("\\xa0", "").replace("’", "'").replace("é", "e").replace("É", "E")
        s = s.replace("è", "e").replace("\\n", "").replace(",", ".").replace(" ", "")
        return s

    df2.columns = [clean_col(col) for col in df2.columns]
                """, language="python")
                
    st.markdown('<p class="small-font"><li>Standardisation des noms de colonnes</li></p>', unsafe_allow_html=True)
    with st.expander(""):
        st.code("""dico_colonnes2 = {
    "PointdelivraisonPDL": "Numero_PDL",
    "FacturationFactureN°": "Numero_facture",
    'PointdelivraisonSegment':"Segment",
    'ReferencesContrat':"Numero_contrat",
    "ComptageFormuleTarifaired'Acheminement":"Formule_tarifaire_acheminement",
    'PUISSANCESSOUSCRITESBASE':"Puissance_souscrite",
    "FacturationDateFacture": "Date_facture",
    "PeriodedeconsommationDebutdeperiode": "Date_debut_periode",
    "PeriodedeconsommationFindeperiode": "Date_fin_periode",
    'PointdelivraisonClientfinal' : "Client_final", 
    'DetailsiteTotalHorsTVAMontant(€)': "Total_HTVA",
    'DetailsiteTOTALTTCMontant(€)': "Total_TTC",
    'DetailsiteTVA5.5%Montant(€)' : "TVA_5.5",
    'DetailsiteTVA20%Montant(€)' :"TVA_20",
    'PrestationsGRDMontant(€)': "Prestations_GRD", 
    'FraisdegestionMontantHT(€)' : "Frais_remises_supplementaires",

    "ContributionTarifaireacheminementMontant(€)" : "CTA",
    "ContributionauServicePublicdel'ElectriciteMontant(€)" : "CSPE", 

    'Consommationparpostehorosaisonnier(kWh)BASE':"Consommation_BASE", 
    'Consommationparpostehorosaisonnier(kWh)HP':"Consommation_HP", 
    'Consommationparpostehorosaisonnier(kWh)HC':"Consommation_HC", 
    'Consommationparpostehorosaisonnier(kWh)POINTE':"Consommation_POINTE", 
    'Consommationparpostehorosaisonnier(kWh)HPH':"Consommation_HPH", 
    'Consommationparpostehorosaisonnier(kWh)HCH':"Consommation_HCH", 
    'Consommationparpostehorosaisonnier(kWh)HPE':"Consommation_HPB", 
    'Consommationparpostehorosaisonnier(kWh)HCE':"Consommation_HCB", 
    'ConsommationenergieactiveVolume(kWh)':"Consommation_totale",
    
    'ConsommationenergieactiveTotal(€)':"Tarif_consommation_energie_active" ,
    'CapaciteMontant(€)': "Capacite" , 
    'GarantieOrigineMontant(€)': 'Garantie_origine' , 
    "Certificatd'economied'energieMontant(€)": "CEE" , 
    'GarantieOrigineincluseMontant(€)': "Garantie_origines_inclus", 
    "Certificatd'economied'energieinclusMontant(€)": "CEE_inclus", 
    'AbonnementMontant(€)':"Abonnement", 
    'AbonnementOptions(€)': "Abonnement_option",
    'AbonnementTotal(€)': "Tarif_total_abonnement",
     
    'DepassementsMontant(€)': "Depassement",
    'DepassementBT>36kVAQuantite(h)':"Depassement_puissance_souscrite", 
    'EnergiereactiveMontant(€)': "Energie_reactive",
    'ComposantedeGestionMontant(€)': "Composante_gestion", 
    'ComposantedeGestiondesAutoproducteursMontant(€)': "Composante_gestion_autoproducteurs" , 
    'ComposantedeComptageMontant(€)': "Composante_comptage", 
    'PartfixeComposantedesoutirageMontant(€)' :"Part_fixe_composante_soutirage" , 
    'PartvariableComposantedesoutirageMontant(€)': 'Part_variable_composante_soutirage', 
    'ComposantealimentationscomplementairesMontant(€)':"Composante_alimentations_complementaires" , 
    'ComposantealimentationsdesecoursMontant(€)': 'Composante_alimentations_secours' , 
    'ComposantederegroupementMontant(€)':'Composante_regroupement' ,
    'PointdelivraisonAdresselieudeconsommation':'Adresse_facture' ,
    'PointdelivraisonCodepostallieudeconsommation':'CP_facture',
    'PointdelivraisonCommunelieudeconsommation':'Ville_facture'} )

             """, language="python")
             
    st.markdown('<p class="small-font"><li>Renommage des colonnes</li></p>', unsafe_allow_html=True)
    with st.expander(""):
        st.code("""
    df_renomme2 = df2.rename(columns=dico_colonnes2)[[col for col in dico_colonnes2.values() if col in df2.rename(columns=dico_colonnes2).columns]].copy()
                """, language="python")

    st.markdown('<p class="small-font"><li>Création de nouvelles colonnes</li></p>', unsafe_allow_html=True)
    with st.expander(""):
        st.code("""
    df_renomme2["Total_TVA"] = df_renomme2["TVA_5.5"] + df_renomme2["TVA_20"]
    df_renomme2["Tarif_taxes_contributions_locales"] = df_renomme2["CSPE"] + df_renomme2["CTA"]
    df_renomme2["Tarif_acheminement"] = (
        df_renomme2["Depassement"] + df_renomme2["Energie_reactive"] + df_renomme2["Composante_gestion"] +
        df_renomme2["Composante_gestion_autoproducteurs"] + df_renomme2["Composante_comptage"] +
        df_renomme2["Part_fixe_composante_soutirage"] + df_renomme2["Part_variable_composante_soutirage"] +
        df_renomme2["Composante_alimentations_complementaires"] + df_renomme2["Composante_alimentations_secours"] +
        df_renomme2["Composante_regroupement"]
    )
    df_renomme2["Tarif_fourniture"] = (
        df_renomme2["Tarif_consommation_energie_active"] + df_renomme2["Capacite"] +
        df_renomme2["Garantie_origine"] + df_renomme2["CEE"] +
        df_renomme2["Garantie_origines_inclus"] + df_renomme2["CEE_inclus"] +
        df_renomme2["Tarif_total_abonnement"]
    )
    df_renomme2["Duree_periode_consommation"] = (
        df_renomme2["Date_fin_periode"] - df_renomme2["Date_debut_periode"]
    ).dt.days
                """, language="python")

    st.markdown('<p class="small-font"><li>Format et normalisation</li></p>', unsafe_allow_html=True)
    with st.expander(""):
                st.code("""
# modification des formats texte en string
df_renomme2["Numero_PDL"] = df_renomme2["Numero_PDL"].astype("string").str.strip().str.replace(r"\.0$", "", regex=True)
df_renomme2["Adresse_facture"] = df_renomme2["Adresse_facture"].astype("string").str.strip().str.replace(r"\.0$", "", regex=True)
df_renomme2['CP_facture'] = df_renomme2['CP_facture'].astype("string").str.strip().str.replace(r"\.0$", "", regex=True)
df_renomme2['Ville_facture'] = df_renomme2['Ville_facture'].astype("string").str.strip().str.replace(r"\.0$", "", regex=True)
df_renomme2["Numero_facture"] = df_renomme2["Numero_facture"].astype("string").str.strip().str.replace(r"\.0$", "", regex=True)


# Conversion des dates
df_renomme2["Date_facture"] = pd.to_datetime(df_renomme2["Date_facture"], dayfirst=True, errors="coerce")
df_renomme2["Date_debut_periode"] = pd.to_datetime(df_renomme2["Date_debut_periode"], dayfirst=True, errors="coerce")
df_renomme2["Date_fin_periode"] = pd.to_datetime(df_renomme2["Date_fin_periode"], dayfirst=True, errors="coerce")
                """, language="python")

        # ------------------ FUSION ------------------

    st.markdown('<p class="small-font"><b>3. Fusion des données des deux fournisseurs</b></p>', unsafe_allow_html=True) 

    st.markdown('<p class="small-font"><li>Fusion sur les colonnes communes</li></p>', unsafe_allow_html=True)
    with st.expander(""):
        st.markdown('<p class="small-font"><b>Objectif : créer un seul jeu de données uniforme</b></p>', unsafe_allow_html=True)
        st.code("""
    colonnes_communes = [
        "Numero_PDL", "Numero_facture", "Segment", "Formule_tarifaire_acheminement",
        "Puissance_souscrite", "Date_facture", "Date_debut_periode", "Date_fin_periode",
        "Duree_periode_consommation", "Nom_fournisseur", "Client_final", "Tarif_acheminement",
        "Tarif_taxes_contributions_locales", "Tarif_fourniture", "Total_TTC", "Total_TVA", "Total_HTVA",
        "Consommation_BASE", "Consommation_HP", "Consommation_HC", "Consommation_POINTE", "Consommation_HPH",
        "Consommation_HCH", "Consommation_HPB", "Consommation_HCB", "Consommation_totale", "Depassement",
        "Depassement_puissance_souscrite", "Prestations_GRD", "Frais_remises_supplementaires"
    ]
    df1_filtre = df_renomme1[colonnes_communes]
    df2_filtre = df_renomme2[colonnes_communes]
    df_fusionne = pd.concat([df1_filtre, df2_filtre], ignore_index=True)
                """, language="python")

    st.success("✅ Les jeux de données ont été nettoyés, harmonisés et fusionnés avec succès.")


# === PAGE 4 : Fichier Final =======================================================================================
if page == "Fichier Final":
    st.subheader("Fichier Final")

    try:
        # Chargement des données
        df1 = load_volterres_data(df1_path)
        df2 = load_lbe_data(df2_path)
        df_fusionne = load_df_fusionne(df_fusionne_path)
        df_fusionne["Date_facture"] = pd.to_datetime(df_fusionne["Date_facture"], errors="coerce")

                    # modification des formats 
        df_fusionne["Numero_PDL"] = df_fusionne["Numero_PDL"].astype("string").str.strip().str.replace(r"\.0$", "", regex=True)
        df_fusionne["Numero_facture"] = df_fusionne["Numero_facture"].astype("string").str.strip().str.replace(r"\.0$", "", regex=True)
        df_fusionne["Date_debut_periode"] = pd.to_datetime(df_fusionne["Date_debut_periode"], dayfirst=True, errors="coerce")
        df_fusionne["Date_fin_periode"] = pd.to_datetime(df_fusionne["Date_fin_periode"], dayfirst=True, errors="coerce")




        # 📏 Dimensions (nombre de colonnes uniquement)
        st.markdown("**📏 Nombre de colonnes par fichier :**")
        st.markdown(f"- Volterres : **{df1.shape[1]}** colonnes")
        st.markdown(f"- LBE : **{df2.shape[1]}** colonnes")
        st.markdown(f"- Fichier final Fusionné : **{df_fusionne.shape[1]}** colonnes")

        # 📑 Liste des colonnes et types dans un expander
        with st.expander("Liste des colonnes et types"):
            colonnes_types = pd.DataFrame({
                "Nom de la colonne": df_fusionne.columns,
                "Type": df_fusionne.dtypes.values
            })
            st.dataframe(colonnes_types, use_container_width=True)

        st.markdown("""
        <p>Nous avons selectionné 30 colonnes qui nous ont semblé utiles à l'analyse des factures d'électricité.</p> 
        <p>Certaines colonnes des factures que nous avions conservées n'ont pas été utilisées pendant le stage par manque de temps (Heures pleines/heures creuses),
        et d'autres devront être ajoutés au modèle pour pouvoir suivre la production d'énergie dans le cadre des projets en cours.</p> 
    
        """, unsafe_allow_html=True)


        

        # 🗓️ Dates de facturation par fournisseur
        st.markdown("**🗓️ Périodes de facturation par fournisseur :**")

        # Calcul des dates min/max par fournisseur
        dates_par_fournisseur = df_fusionne.groupby("Nom_fournisseur").agg(
            Date_debut_facturation=("Date_facture", "min"),
            Date_fin_facturation=("Date_facture", "max")
        ).reset_index()

        # Formater les dates pour affichage
        dates_par_fournisseur["Date_debut_facturation"] = dates_par_fournisseur["Date_debut_facturation"].dt.strftime("%d/%m/%Y")
        dates_par_fournisseur["Date_fin_facturation"] = dates_par_fournisseur["Date_fin_facturation"].dt.strftime("%d/%m/%Y")

        # Affichage dans un tableau Streamlit
        st.dataframe(dates_par_fournisseur, hide_index=True)

        # 🔍 Aperçu du fichier fusionné
        st.markdown("**🔍 Aperçu du fichier fusionné :**")        
        st.markdown(f"Dimensions du fichier : {df_fusionne.shape}")

        st.dataframe(df_fusionne.head(30), use_container_width=True, height=200)

        st.markdown("✅ Le fichier fusionné est chargé et prêt à être utilisé dans le modèle Power BI.")

    except Exception as e:
        st.error(f"❌ Une erreur est survenue lors du chargement des données : {e}")


# === PAGE 5 : Statistiques =======================================================================================
if page == "Statistiques et visualisations":

    df_fusionne = load_df_fusionne(df_fusionne_path)

    st.subheader("Quelques Visualisations")

    # Liste ordonnée des fournisseurs
    fournisseurs = df_fusionne['Nom_fournisseur'].value_counts().index.tolist()

    # Couleurs personnalisées
    couleurs_personnalisees = ['#74C3B7', '#F9BE6B', '#BBD092']

    # Mapping fournisseur -> couleur
    couleur_map = {fournisseur: couleur for fournisseur, couleur in zip(fournisseurs, couleurs_personnalisees)}

    # Données factures
    factures_par_fournisseur = df_fusionne['Nom_fournisseur'].value_counts().reset_index()
    factures_par_fournisseur.columns = ['Nom_fournisseur', 'count']

    # Données consommation MW
    conso_par_fournisseur = (
        df_fusionne.groupby('Nom_fournisseur')['Consommation_totale']
        .sum()
       . div(1000)  # diviser par 1000 pour convertir en MW
        .reset_index()
    )
    
    conso_par_fournisseur['Consommation_totale'] = conso_par_fournisseur['Consommation_totale'].round(0)

# Création des colonnes dans Streamlit
    col1, col2 = st.columns(2)

    #Affichage du camembert colonne 1
    with col1:
        fig_pie_factures = px.pie(
            factures_par_fournisseur,
            names='Nom_fournisseur',
            values='count',
            color='Nom_fournisseur',
            color_discrete_map=couleur_map
        )
        fig_pie_factures.update_traces(
            textinfo='label+percent+value',
            textfont_size=16,
            marker=dict(line=dict(color='#fff', width=1)),
            showlegend=False
        )
        fig_pie_factures.update_layout(
            annotations=[{
                'text': "Nombre de factures par fournisseur",
                'x': 0.5, 'y': -0.15,
                'xref': 'paper', 'yref': 'paper',
                'showarrow': False,
                'font': {'size': 20}
            }],
            height=320,
            margin=dict(t=40, b=80, l=40, r=40)
        )
        st.plotly_chart(fig_pie_factures, use_container_width=True)


    
    #Affichage du camembert colonne 2
    with col2:
        fig_pie_conso = px.pie(
            conso_par_fournisseur,
            names='Nom_fournisseur',
            values='Consommation_totale',
            color='Nom_fournisseur',
            color_discrete_map=couleur_map
        )
        
        fig_pie_conso.update_traces(
            textinfo='label+percent+value',
            textfont_size=16,
            marker=dict(line=dict(color='#fff', width=1)),
            showlegend=False,
            textposition='auto',
        ) 
        fig_pie_conso.update_layout( 
            annotations=[{ 
                'text': "Consommation par fournisseur (MW)", 
                'x': 0.5, 'y': -0.15,
                'xref': 'paper', 'yref': 'paper',
                'showarrow': False,
                'font': {'size': 20}
            }],
            height=320,
            margin=dict(t=40, b=80, l=40, r=40)
        )
        st.plotly_chart(fig_pie_conso, use_container_width=True)


    fig_box = px.box(
        df_fusionne,
        x='Nom_fournisseur',
        y='Total_HTVA',
        title="Répartition de la consommation par fournisseur",
        labels={'Consommation_totale': 'Consommation (kW)'}
    )

    fig_box.update_layout(
    legend_title_text='Fournisseur',  # Titre légende
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5
        )
    )



    # 📦 Boxplot interactif : montant HTVA par PDL selon fournisseur

    # Regrouper les données par PDL et fournisseur
    df_par_pdl = (
        df_fusionne.groupby(["Nom_fournisseur", "Numero_PDL"], as_index=False)
        .agg({
            "Consommation_totale": "sum",
            "Total_HTVA": "sum"
        })
    )

    # Couleurs personnalisées
    couleur_map = {
        'LBE': '#74C3B7',
        'Volterres': '#F9BE6B'
    }

    fig_htva = px.box(
        df_par_pdl,
        x='Nom_fournisseur',
        y='Total_HTVA',
        color='Nom_fournisseur',
        color_discrete_map=couleur_map,
        labels={
            'Total_HTVA': 'Montant total HTVA par PDL (€)',
            'Nom_fournisseur': 'Fournisseur'
        },
        title="💶 Montant HTVA total par PDL",
        hover_data=["Numero_PDL"]
        )

    fig_htva.update_layout(
        legend_title_text="Fournisseur (cliquez pour filtrer)",
        margin=dict(t=60, b=60),
        yaxis_title='Montant HTVA (€)',
        xaxis_title='Fournisseur',
        height=500
        )

    st.plotly_chart(fig_htva, use_container_width=True)

    st.subheader("Statistiques")
    # 📊 Statistiques descriptives globales
    st.markdown("**📊 Statistiques descriptives (colonnes numériques) :**")
    df_description = df_fusionne[["Tarif_acheminement"]].describe().transpose().reset_index()
    df_description.rename(columns={"index": "Colonne"}, inplace=True)
    st.dataframe(df_description, use_container_width=True)


# === PAGE 6 : Conclusion =======================================================================================
if page == "Conclusion":
    
    st.markdown("""
    <h4><strong>Conclusions</strong></h4>
    <p>Le script réalisé avec python en début de stage a permis bien comprendre le contexte du marché d'électricité et la structure des factures des deux fournisseurs.</p> 
    <p>Il a été utilisé plusieurs fois au cours du stage afin d'intégrer les nouvelles factures au modèle Power BI.</p>
    <p>Le fichier transformé a été croisé avec d'autres données (Données de références des PDL, informations sur les marchés, données ENEDIS) pour permettre un suivi des factures et du marché.</p> 
    <p>J'ai eu l'occasion de présenter le rapport Power BI réalisé au Directeur Général des Services ainsi qu'à la responsable des marchés publics au cours d'une réunion organisée à la fin de mon stage.</p> 

    """, unsafe_allow_html=True)

    st.markdown("""
    <h4><strong>Perspectives</strong></h4>

    <p>Le travail réalisé au cours de mon stage (script Pyhton et rapport Power BI) sera complété et enrichi par l'entreprise et les flux seront automatisés.</p> 
    
    <p>Ce travail préliminaire permettra à terme à l'entreprise de mieux maîtriser ses dépenses d'électricité et d'optimiser ses contrats 
    en s'assurant de l'adéquation des besoins de chaque PDL au type de contrat.</p> 
    
    <p>Cela m'a permis de travailler sur des données liées à l'énergie et d'utiliser différents outils (notebook Jupyter, VS Code, Excel, Power BI). 
    J'ai également pu m'imprégner du fonctionnement de l'entreprise et mieux comprendre les attentes des métiers vis à vis de la DSI et de l'équipe Data.</p> 


    """, unsafe_allow_html=True)



