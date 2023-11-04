import os
import pandas as pd
from sqlalchemy import create_engine, text
import uuid

# Paramètres de connexion à la base de données
db_params = {
    'dbname': 'GoldMarbrerie',
    'user': 'wilde.diogene',
    'password': 'Octo2023-%£',
    'host': 'localhost',
    'port': 5432
}

# Chemin vers le dossier contenant les fichiers CSV
data_folder = '/Users/wilde.diogene/Documents/My_Projects/Perso/GoldMarbrerieReporting/data/processed/2022'

# Créer une connexion à la base de données
engine = create_engine(f'postgresql://{db_params["user"]}:{db_params["password"]}@{db_params["host"]}:{db_params["port"]}/{db_params["dbname"]}')

# Fonction pour charger un fichier CSV dans la table 'invoices'
def load_csv_to_table(csv_file_path, engine):
    # Lire le fichier CSV dans un DataFrame
    df = pd.read_csv(csv_file_path, encoding='utf-8-sig')
    
    # Ajouter une colonne ID avec un UUID unique pour chaque ligne
    df['id'] = [uuid.uuid4() for _ in range(len(df))]
    
    # Supprimer les lignes existantes avec les mêmes n_document
    n_documents = df['n_document'].tolist()
    with engine.begin() as conn:  # Use `begin()` to start a transaction context
        # Use `text()` to construct a SQL expression that SQLAlchemy can execute
        delete_statement = text(
            "DELETE FROM invoices WHERE n_document = ANY(:n_document_array)"
        )
        conn.execute(delete_statement, {'n_document_array': n_documents})
    
    # Charger le DataFrame dans la table 'invoices'
    df.to_sql('invoices', engine, if_exists='append', index=False)



# Parcourir tous les fichiers qui commencent par "Invoice" dans le dossier
for file_name in os.listdir(data_folder):
    if file_name.startswith("Invoice") and file_name.endswith(".csv"):
        file_path = os.path.join(data_folder, file_name)
        load_csv_to_table(file_path, engine)
        print(f"Les données de {file_name} ont été chargées dans la table 'invoices'.")

print("Tous les fichiers ont été chargés avec succès.")
