import psycopg2
from psycopg2 import OperationalError


# Parameters for the database connection
db_params = {
    'dbname': 'GoldMarbrerie',
    'user': 'wilde.diogene',
    'password': '',
    'host': 'Localhost',
    'port': '5432'  # typically 5432 for PostgreSQL
}

# SQL statements to create the tables
sql_statements = [
    """
    CREATE TABLE Clients (
        Code CHAR(5) PRIMARY KEY,
        Description TEXT,
        Client_type VARCHAR(255),
        Channel VARCHAR(255),
        Raison_Social VARCHAR(255),
        Nom TEXT,
        Prenom TEXT,
        Adresse TEXT, 
        Code_psotal INTEGER, 
        Ville VARCHAR(255), 
        Telephone VARCHAR(255), 
        SIRET VARCHAR(255), 
        Nom_du_contact TEXT

    );
    """,
    """
    CREATE TABLE Products (
        Reference VARCHAR(255) PRIMARY KEY,
        Description TEXT,
        Famille VARCHAR(255),
        Prix_vente_HT DECIMAL, 
        Prix_achat DECIMAL, 
        TVA DECIMAL,
        Prix_vente_TTC DECIMAL,
        Last_update DATE

    );
    """,
    """
    CREATE TABLE Invoices (
        N_document CHAR(9) PRIMARY KEY,
        Type_document VARCHAR(255),
        Date DATE,
        Famille VARCHAR(255), 
        Ligne VARCHAR(255),
        Reference VARCHAR(255),
        Designation TEXT,
        Quantite DECIMAL,
        PU_Achat DECIMAL,
        Montant_HT_x DECIMAL,
        Remise DECIMAL,
        Marge DECIMAL,
        Date_saisie DATE,
        Raison_sociale TEXT,
        Nom_du_client TEXT,
        Prenom_du_client TEXT,
        Montant_HT_Y DECIMAL,
        Montant_TVA DECIMAL,
        Montant_TTC DECIMAL,
        Type_client VARCHAR(255)

    );
    """,
    """
    CREATE TABLE Entity (
        Code CHAR(5) PRIMARY KEY,
        Description TEXT
    );
    """
]

# Establish the connection
with psycopg2.connect(**db_params) as conn:
    with conn.cursor() as cursor:
        for sql in sql_statements:
            cursor.execute(sql)

print("Tables created successfully!")
