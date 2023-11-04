import pandas as pd
import os
import re
from unidecode import unidecode

# 1. Lire les deux fichiers csv
directory_path = '/Users/wilde.diogene/Documents/My_Projects/Perso/GoldMarbrerieReporting/data/processed/2022'
sales_details_path = os.path.join(directory_path, "Sales_details_aggregated_2022.csv")
sales_header_path = os.path.join(directory_path, "Journal_des_ventes_2022.csv")

Sales_details = pd.read_csv(sales_details_path, encoding='utf-8-sig')
Sales_header = pd.read_csv(sales_header_path, encoding='utf-8-sig')

# Fonction pour normaliser les noms de colonnes
def normalize_column_names(df):
    # Retirer les accents, remplacer les espaces et caractères spéciaux par des underscores
    # et convertir en minuscules
    df.columns = [unidecode(col).lower().replace(' ', '_') for col in df.columns]
    # Remplacer les caractères non-alphanumériques restants par des underscores
    df.columns = [re.sub(r'\W+', '_', col) for col in df.columns]
    return df


# 2. Renommez la colonne "N°" en "N° document"
Sales_details.rename(columns={'N°': 'N° document'}, inplace=True)

# 3. Supprimer les 3 premiers caractères "N° " dans la colonne "N° document" de Sales_details
Sales_details['N° document'] = Sales_details['N° document'].str[3:]


# Fonction pour renommer les colonnes
def rename_columns(df):
    # Remplace les espaces et caractères spéciaux par '_'
    df.columns = [re.sub(r'\W+', '_', col) for col in df.columns]
    return df

# Fonction pour remplacer les virgules par des points pour les colonnes de nombre
def convert_comma_decimal_to_float(df, columns):
    for column in columns:
        # Vérifiez d'abord si la colonne est de type object pour éviter les erreurs avec les colonnes non-string
        if df[column].dtype == 'object':
            # Remplacez les virgules par des points et convertissez en float
            df[column] = df[column].str.replace(',', '.').astype(float)
    return df

# 4. Fonction pour renommer les colonnes
Sales_details = rename_columns(Sales_details)
Sales_header = rename_columns(Sales_header)

# Appliquer la normalisation des noms de colonnes
Sales_details = normalize_column_names(Sales_details)
Sales_header = normalize_column_names(Sales_header)

# 5. Remplacez les sauts de ligne par des espaces dans la colonne "Désignation"
Sales_details['designation'] = Sales_details['designation'].str.replace('\n', ' ')

# Fonction pour déterminer la colonne Type_client
def determine_type(row):
    if pd.isna(row['raison_sociale']) or row['raison_sociale'] == '':
        return 'Particulier'
    else:
        return 'Professionnel'

# 6. Renommer les colonnes pour matcher avec les colonnes de la base de donnée
Sales_details.rename(columns={
    'type': 'type_document',
    '_rem': 'remise',
    '_marge': 'marge',
    # Ajoutez d'autres colonnes à renommer ici
}, inplace=True)


# 8. Après avoir effectué la jointure alimenter la colonne Type_client
Sales_header['type_client'] = Sales_header.apply(determine_type, axis=1)


# Convertir les colonnes de date au format YYYY-MM-DD
Sales_details['date'] = pd.to_datetime(Sales_details['date'], format='%d/%m/%Y').dt.strftime('%Y-%m-%d')
Sales_header['date_saisie'] = pd.to_datetime(Sales_header['date_saisie'], format='%d/%m/%Y').dt.strftime('%Y-%m-%d')

# Utilisez cette fonction pour convertir les colonnes numériques
numeric_columns_details = ['quantite', 'pu_achat', 'montant_ht','remise','marge']  # Remplacez ceci par les noms réels de vos colonnes numériques
numeric_columns_header = ['montant_ht','montant_tva','montant_ttc']  # Remplacez ceci par les noms réels de vos colonnes numériques
Sales_details = convert_comma_decimal_to_float(Sales_details, numeric_columns_details)
Sales_header = convert_comma_decimal_to_float(Sales_header, numeric_columns_header)


# 9. Sauvegardez le résultat dans un fichier CSV
output_csv_path = os.path.join(directory_path, "Invoices_2022.csv")
Sales_details.to_csv(output_csv_path, index=False, encoding='utf-8-sig')
output_csv_path = os.path.join(directory_path, "Clients_2022.csv")
Sales_header.to_csv(output_csv_path, index=False, encoding='utf-8-sig')
