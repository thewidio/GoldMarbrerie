import pandas as pd
import os

# SALES DETAILS FILE AGGREGATION

# Chemin du dossier contenant les fichiers Sales_details à aggréger
directory_path_2022 = '/Users/wilde.diogene/Documents/My_Projects/Perso/GoldMarbrerieReporting/data/raw/2022/Sales_details'
output_directory_2022 = '/Users/wilde.diogene/Documents/My_Projects/Perso/GoldMarbrerieReporting/data/processed/2022'

# Liste pour stocker les données de chaque fichier
all_dataframes = []

# Parcourez chaque fichier dans le dossier
for filename in os.listdir(directory_path_2022):
    if filename.endswith(".xlsx"):  # Assurez-vous de traiter seulement les fichiers Excel
        filepath = os.path.join(directory_path_2022, filename)
        
        # Lisez le fichier Excel dans un DataFrame
        df = pd.read_excel(filepath, engine='openpyxl')
        all_dataframes.append(df)

# Concaténez tous les DataFrames en un seul
concatenated_df = pd.concat(all_dataframes, ignore_index=True)

# Sauvegardez le DataFrame consolidé dans un nouveau fichier Excel dans le dossier de fichieer Processed
output_file_path = os.path.join(output_directory_2022, "Sales_details_aggregated_2022.csv")
#concatenated_df.to_excel(output_file_path, index=False, engine='openpyxl')
concatenated_df.to_csv(output_file_path, index=False, encoding='utf-8-sig')

print("Les fichiers ont été agrégés avec succès!")


# JOURNAL DES VENTES

# Chemin du dossier pour le fichier Journal des ventes
directory_path_2022_jv = '/Users/wilde.diogene/Documents/My_Projects/Perso/GoldMarbrerieReporting/data/raw/2022'
sales_header_path = os.path.join(directory_path_2022_jv , "Journal des ventes_2022.xlsx")


Sales_header = pd.read_excel(sales_header_path, engine='openpyxl')

# Sauvegardez le résultat dans un fichier CSV
output_csv_path = os.path.join(output_directory_2022, "Journal_des_ventes_2022.csv")
Sales_header.to_csv(output_csv_path, index=False, encoding='utf-8-sig')