    #import des librairies 
import pandas as pd
import openpyxl
import os 
import numpy as np
from pathlib import Path

## Récupérer le dossier du script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construire le chemin vers le dossier "Fichiers"
fichiers_dir = os.path.join(current_dir, "Fichiers")

# Noms des fichiers Excel
file1 = "VOLTERRES_Anonyme.xlsx"
file2 = "LBE_Anonyme.xlsx"

# Construire les chemins complets vers les fichiers
df1_path = os.path.join(fichiers_dir, file1)
df2_path = os.path.join(fichiers_dir, file2)

# Charger les fichiers Excel
df1 = pd.read_excel(df1_path)
df2 = pd.read_excel(df2_path, header=[0, 1])  # si ton fichier LBE a un header multi-niveau, sinon header=0

print("✅ Fichiers chargés avec succès.")
print("Shape du dataframe Volterre:", df1.shape)
print("Shape du dataframe Lbe:", df2.shape)

# df1 / VOLTERRES
    # dictionnaire : renommer colonnes 
dico_colonnes1={
    "Numéro de PDL" :"Numero_PDL" ,
    "N° de facture" :"Numero_facture" ,
    "Date de facturation" :"Date_facture"  ,
    "Date de début de relève" : "Date_debut_periode",
    "Date de fin de relève" :"Date_fin_periode" , 
    "Transport et distribution (€HT)" : "Tarif_acheminement",
    "Taxes et contributions locales (€HTVA)": "Tarif_taxes_contributions_locales",
    "Électricité et options associées (€HT)" : "Tarif_fourniture",
    "Total à payer (€TTC)" :"Total_TTC",
    "Total TVA (€)": "Total_TVA",
    "Segment":"Segment",
    "Numéro de contrat":"Numero_contrat",
    "Formule Tarifaire d'Acheminement":"Formule_tarifaire_acheminement",
    "Puissance souscrite":"Puissance_souscrite",
    'Consommation Heures pleines saison haute (kWh)':"Consommation_HPH",
    'Consommation Heures creuses saison haute (kWh)':"Consommation_HCH",
    'Consommation Heures pleines saison basse (kWh)':"Consommation_HPB",
    'Consommation Heures creuses saison basse (kWh)':"Consommation_HCB",
    'Consommation Base (kWh)':"Consommation_BASE", 
    'Consommation Heures pleines (kWh)':"Consommation_HP", 
    'Consommation Heures creuses (kWh)':"Consommation_HC", 
    'Consommation Pointe (kWh)':"Consommation_POINTE",
    'Consommation totale (kWh)':"Consommation_totale",
    'dont CEE (€HT)': "CEE",
    'dont Capacité (€HT)': "Capacite" ,
    "dont Garanties d'origine (€HT)":'Garantie_origine',
    'CTA (€HTVA)':"CTA",              
    'CSPE (€HTVA)':"CSPE", 
    'dont Dépassement de puissance (€HT)':"Depassement",
    'Dépassement de puissance souscrite (h ou kWh)' : "Depassement_puissance_souscrite",
    'Prestations GRD (€HT)' : "Prestations_GRD", 
    'Frais et remises (€HT)':"Frais_remises_supplementaires",
    'Adresse':"Adresse_facture",
    'Code postal':'CP_facture',
    'Ville':'Ville_facture'} 

    #renommer 
df_renomme1 = df1.rename(columns=dico_colonnes1)[[col for col in dico_colonnes1.values() if col in df1.rename(columns=dico_colonnes1).columns]].copy()

print("Colonnes actuelles Volterre :", df_renomme1.columns.tolist())

df_renomme1=df_renomme1.fillna(0)

    # création des colonnes manquantes 
        #Total_HTVA
df_renomme1["Total_HTVA"] = (
    df_renomme1["Tarif_acheminement"] +
    df_renomme1["Tarif_taxes_contributions_locales"] +
    df_renomme1["Tarif_fourniture"]+
    df_renomme1["Prestations_GRD"]+
    df_renomme1["Frais_remises_supplementaires"])

        #Duree_periode_conso
df_renomme1['Duree_periode_consommation'] = (
    df_renomme1['Date_fin_periode'] - 
    df_renomme1['Date_debut_periode']).dt.days


# Détection et suppression des lignes entièrement vides  (toutes les colonnes nulles)
lignes_vides1 = df_renomme1[df_renomme1.isnull().all(axis=1)]
print("🔍 Nombre de lignes entièrement vides :", len(lignes_vides1))
df_renomme1 = df_renomme1.dropna(how='all')

# Exemple de nettoyage complet
df_renomme1.replace(r'^\s*$', np.nan, regex=True, inplace=True)
df_renomme1.replace(['nan', 'NaN', 'None'], np.nan, inplace=True)
df_renomme1 = df_renomme1.dropna(how='all')

print("✅ Lignes entièrement vides supprimées.")

        #Nom_fournisseur
df_renomme1["Nom_fournisseur"] = "Volterres"

        #Client_final
df_renomme1["Client_final"] = "SPL LES EAUX DU SAGE"   

    #modification des formats 
        #en string
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

        #en float
df_renomme1[["Consommation_HPH","Garantie_origine","Capacite","CEE","Consommation_totale","Consommation_HCB","Consommation_HPB","Consommation_HCH"]] = df_renomme1[["Consommation_HPH","Garantie_origine","Capacite","CEE","Consommation_totale","Consommation_HCB","Consommation_HPB","Consommation_HCH"]].astype(float)   

    #vérification des formats et du nombre de valeur NaN des colonnes
print("le nombre de valeur NaN par colonne est: "  ,df_renomme1.isna().sum())
print("les types des colonnes sont : ", df_renomme1.dtypes)
    #remplacement des Nan par des 0
df_renomme1=df_renomme1.fillna(0)


# df2 / LBE
    #les noms des colonnes sont réparties sur 2 lignes 
df2 = pd.read_excel(df2_path, header=[0, 1])

    #nettoyage des noms 
def clean_col(col):
    if isinstance(col, tuple):
        col = " ".join([str(c) for c in col if c])

    s = str(col).strip()
    s = s.replace("\xa0", "")     
    s = s.replace("’", "'")       
    s = s.replace("é", "e")
    s = s.replace("É", "E")
    s = s.replace("è", "e")
    s = s.replace("\n", "")      
    s = s.replace(",", ".")       
    s = s.replace(" ", "")       

    return s
df2.columns = [clean_col(col) for col in df2.columns]
print("Colonnes transformées Lbe :", df2.columns.tolist())

    #dictionnaire 
dico_colonnes2 = {
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
    'PointdelivraisonCommunelieudeconsommation':'Ville_facture'} 


df_renomme2 = df2.rename(columns=dico_colonnes2)[[col for col in dico_colonnes2.values() if col in df2.rename(columns=dico_colonnes2).columns]].copy()

# Remplacement de valeurs vides ou fausses avant conversion
df_renomme2.replace(r'^\s*$', pd.NA, regex=True, inplace=True)
df_renomme2.replace(['nan', 'NaN', 'None'], pd.NA, inplace=True)

print("Colonnes actuelles Lbe :", df_renomme2.columns.tolist())
   #vérification des formats et du nombre de valeur NaN des colonnes
print("le nombre de valeur NaN par colonne Lbe est: "  ,df_renomme2.isna().sum())
print("les types des colonnes Lbe sont : ", df_renomme2.dtypes)

    # modification des formats 
df_renomme2["Numero_PDL"] = df_renomme2["Numero_PDL"].astype("string").str.strip().str.replace(r"\.0$", "", regex=True)
df_renomme2["Adresse_facture"] = df_renomme2["Adresse_facture"].astype("string").str.strip().str.replace(r"\.0$", "", regex=True)
df_renomme2['CP_facture'] = df_renomme2['CP_facture'].astype("string").str.strip().str.replace(r"\.0$", "", regex=True)
df_renomme2['Ville_facture'] = df_renomme2['Ville_facture'].astype("string").str.strip().str.replace(r"\.0$", "", regex=True)
df_renomme2["Numero_facture"] = df_renomme2["Numero_facture"].astype("string").str.strip().str.replace(r"\.0$", "", regex=True)


# Conversion des dates
df_renomme2["Date_facture"] = pd.to_datetime(df_renomme2["Date_facture"], dayfirst=True, errors="coerce")
df_renomme2["Date_debut_periode"] = pd.to_datetime(df_renomme2["Date_debut_periode"], dayfirst=True, errors="coerce")
df_renomme2["Date_fin_periode"] = pd.to_datetime(df_renomme2["Date_fin_periode"], dayfirst=True, errors="coerce")

# Vérification immédiate
print("Types après conversion :")
print(df_renomme2[["Date_facture", "Date_debut_periode", "Date_fin_periode"]].dtypes)


    # création des colonnes manquantes 
        #Total_TVA 
df_renomme2["Total_TVA"] = (
    df_renomme2["TVA_5.5"] +   
    df_renomme2["TVA_20"])

        #Total_taxes_contributions_locales
df_renomme2["Tarif_taxes_contributions_locales"] = (
    df_renomme2["CSPE"] +
    df_renomme2["CTA"])

        #Tarif_acheminement
df_renomme2["Tarif_acheminement"]=  (
    df_renomme2["Depassement"] +   
    df_renomme2["Energie_reactive"]+
    df_renomme2["Composante_gestion"] +   
    df_renomme2["Composante_gestion_autoproducteurs"]+
    df_renomme2["Composante_comptage"] +   
    df_renomme2["Part_fixe_composante_soutirage"]+
    df_renomme2['Part_variable_composante_soutirage']+
    df_renomme2["Composante_alimentations_complementaires"] +   
    df_renomme2["Composante_alimentations_secours"]+
    df_renomme2["Composante_regroupement"]
    )

        #Total_fourniture
df_renomme2["Tarif_fourniture"]=  (
    df_renomme2["Tarif_consommation_energie_active" ] +   
    df_renomme2["Capacite"]+
    df_renomme2['Garantie_origine'] +   
    df_renomme2["CEE"]+
    df_renomme2["Garantie_origines_inclus"] +   
    df_renomme2["CEE_inclus"]+
    df_renomme2[ "Tarif_total_abonnement"]
    )
    
        #Duree_periode_consommation
df_renomme2['Duree_periode_consommation'] = (df_renomme2['Date_fin_periode'] - df_renomme2['Date_debut_periode']).dt.days

        #rajout des unites dans puissance souscrite 
df_renomme2['Puissance_souscrite'] = df_renomme2['Puissance_souscrite'].astype(str) + ' kVA'

        #suppression des lignes vides 
lignes_vides = df_renomme2[df_renomme2.isnull().all(axis=1)]
print("🔍 Nombre de lignes entièrement vides :", len(lignes_vides))
df_renomme2 = df_renomme2.dropna(how='all')
df_renomme2.replace(r'^\s*$', np.nan, regex=True, inplace=True)
df_renomme2.replace(['nan', 'NaN', 'None'], np.nan, inplace=True)
df_renomme2 = df_renomme2.dropna(how='all')

print("✅ Lignes entièrement vides supprimées.")

    # création de colonne 
        #Nom_fournisseur
df_renomme2["Nom_fournisseur"] = "LBE"


    # dictionnaires Formule_tarifaire_acheminement
dico_Formule_tarifaire_acheminement = { 
    "BT INF 36 kVA Courte Utilisation": "BT ≤ 36 kVA CU-BASE", 
    "BT INF 36 kVA Courte Utilisation associée à deux saisons":"BT ≤ 36 kVA CU-4 SAISONS",
    "BT INF 36 kVA Longue Utilisation":"BT ≤ 36 kVA LU",
    "BT INF 36 kVA Moyenne Utilisation":"BT ≤ 36 kVA MU-HP/HC",
    "BT INF 36 kVA Moyenne Utilisation associée à deux saisons":"BT ≤ 36 kVA MU-4 SAISONS"}
df_renomme2["Formule_tarifaire_acheminement"]=df_renomme2["Formule_tarifaire_acheminement"].replace(dico_Formule_tarifaire_acheminement)

print("les types des colonnes de LBE sont : ", df_renomme2.dtypes)

    #format
        #string
df_renomme2["Numero_contrat"] = df_renomme2["Numero_contrat"].astype("string").str.strip().str.replace(r"\.0$", "", regex=True)
df_renomme2["Formule_tarifaire_acheminement"] = df_renomme2["Formule_tarifaire_acheminement"].astype("string").str.strip().str.replace(r"\.0$", "", regex=True)
df_renomme2["Nom_fournisseur"] = df_renomme2["Nom_fournisseur"].astype("string").str.strip().str.replace(r"\.0$", "", regex=True)
df_renomme2["Puissance_souscrite"] = df_renomme2["Puissance_souscrite"].astype("string").str.strip().str.replace(r"\.0$", "", regex=True)
df_renomme2["Client_final"] = df_renomme2["Client_final"].astype("string").str.strip().str.replace(r"\.0$", "", regex=True)

        #float
df_renomme2[["Depassement","Consommation_HPH","Garantie_origine","Capacite","CEE","Consommation_totale","Consommation_HCB","Consommation_HPB","Consommation_HCH"]] = df_renomme2[["Depassement","Consommation_HPH","Garantie_origine","Capacite","CEE","Consommation_totale","Consommation_HCB","Consommation_HPB","Consommation_HCH"]].astype(float)

# Étape : Colonnes catégorielles
cat_cols = ["Formule_tarifaire_acheminement", "Nom_fournisseur", "Client_final", "Segment"]
df_renomme1[cat_cols] = df_renomme1[cat_cols].astype("category")
df_renomme2[cat_cols] = df_renomme2[cat_cols].astype("category")

# FUSION 
colonnes_communes = ["Numero_PDL",
    "Numero_facture",
    "Segment",
    "Formule_tarifaire_acheminement",
    "Puissance_souscrite",
    "Date_facture",
    "Date_debut_periode",
    "Date_fin_periode",
    "Duree_periode_consommation",
    "Nom_fournisseur",
    "Client_final",
    "Tarif_acheminement",
    "Tarif_taxes_contributions_locales",
    "Tarif_fourniture",
    "Total_TTC",
    "Total_TVA",
    "Total_HTVA",
    "Consommation_BASE", 
    "Consommation_HP", 
    "Consommation_HC", 
    "Consommation_POINTE", 
    "Consommation_HPH", 
    "Consommation_HCH", 
    "Consommation_HPB", 
    "Consommation_HCB", 
    "Consommation_totale",
    "Depassement",
    "Depassement_puissance_souscrite", 
    "Prestations_GRD" ,                                  
    "Frais_remises_supplementaires",
    ] 

df1_filtre=df_renomme1[colonnes_communes]
df2_filtre=df_renomme2[colonnes_communes]

df_fusionne=pd.concat([df1_filtre,df2_filtre],ignore_index=True)



# Chemin du dossier "Fichiers" (dans le même dossier que le script)
current_dir = os.path.dirname(os.path.abspath(__file__))
fichiers_dir = os.path.join(current_dir, "Fichiers")

# Crée le dossier s'il n'existe pas
os.makedirs(fichiers_dir, exist_ok=True)

# Chemin complet du fichier à exporter
chemin_export = os.path.join(fichiers_dir, "df_fusionne_Anonyme.csv")

df_fusionne.to_csv(chemin_export, index=False, encoding='utf-8-sig', sep=';')

print(f"📁 Fichier exporté avec succès")
print("Nombre de valeurs NaN par colonne après fusion :")
print(df_fusionne.isna().sum())
print("Shape du dataframe après fusion :", df_fusionne.shape)
print("Nombre de valeurs NaN par colonne après fusion :")
print(df_fusionne.isna().sum())

print(df_fusionne.shape)
print(df_fusionne['Nom_fournisseur'].value_counts())

print("les types des colonnes sont : ", df_fusionne.dtypes)

print("✅ Nettoyage terminé.")
print(f"Volterres: {df_renomme1.shape[0]} lignes, {df_renomme1.shape[1]} colonnes")
print(f"LBE      : {df_renomme2.shape[0]} lignes, {df_renomme2.shape[1]} colonnes")

