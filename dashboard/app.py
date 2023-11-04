# Importation des bibliothèques nécessaires
import dash
from dash import dcc
from dash import html
from sqlalchemy import create_engine
import pandas as pd
import plotly.express as px

# Paramètres de connexion à la base de données
db_params = {
    'dbname': 'GoldMarbrerie',
    'user': 'wilde.diogene',
    'password': 'Octo2023-%£',
    'host': 'localhost',
    'port': 5432
}

"""
# ICI LE CODE POUR SE CONNECTER A LA BASE DE DONEES
# Créer une connexion à la base de données
engine = create_engine(f'postgresql://{db_params["user"]}:{db_params["password"]}@{db_params["host"]}:{db_params["port"]}/{db_params["dbname"]}')

# Lire les données de la table 'invoices' dans un DataFrame
df = pd.read_sql('SELECT * FROM invoices', engine)
df['date'] = pd.to_datetime(df['date'], errors='coerce')  # 'coerce' will set invalid parsing as NaT
print(df.head())
"""


# Chemin vers le fichier CSV
csv_file_path = 'data/processed/2022/Invoices_2022.csv'

# Lire les données du fichier CSV dans un DataFrame
df = pd.read_csv(csv_file_path)
df['date'] = pd.to_datetime(df['date'], errors='coerce')  # 'coerce' will set invalid parsing as NaT
print(df.head())


# Initialisation de l'application Dash
app = dash.Dash(__name__)

# Generate options for Month and Year based on the data
months_options = [{'label': month, 'value': month} for month in range(1, 13)]
years_options = [{'label': year, 'value': year} for year in df['date'].dt.year.unique()]

# Définition de la mise en page de l'application
app.layout = html.Div([
    html.H1('Gold Funéraire Performance', style={'textAlign': 'center'}),
    
    # Dropdown for Month Selection
    html.Div([
        html.Label('Mois'),
        dcc.Dropdown(
            id='month-selector',
            options=months_options,
            value=1,  # Default value, January
            className='custom-dropdown'
        ),
    ], style={'width': '48%', 'display': 'inline-block'}),
    
    # Dropdown for Year Selection
    html.Div([
        html.Label('Année'),
        dcc.Dropdown(
            id='year-selector',
            options=years_options,
            value=df['date'].dt.year.max(),  # Default value, current year
            className='custom-dropdown'
        ),
    ], style={'width': '48%', 'display': 'inline-block'}),
    
    # KPIs Display

   html.Div([
    html.Div([
        html.Div([
            html.Div('Ventes mensuelles', className='kpi-title'),
            html.Div(id='progress_month', className='kpi-calculation')
        ], style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center'}),
        html.Div(id='monthly-revenue', className='kpi-value'),
        html.Div('Description of monthly revenue', className='kpi-description')
    ], className='kpi-box'),
    html.Div([
        html.Div([
            html.Div('Ventes annuelles', className='kpi-title'),
            html.Div(id='progress_year', className='kpi-calculation')
        ], style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center'}),
        html.Div(id='annual-revenue', className='kpi-value'),
        html.Div('Description of annual revenue', className='kpi-description')
    ], className='kpi-box')
], style={'display': 'flex', 'justifyContent': 'space-around'})


    # Add more components as needed...
])

# Callbacks to update KPIs
@app.callback(
    [
        dash.dependencies.Output('monthly-revenue', 'children'),
        dash.dependencies.Output('annual-revenue', 'children'),
    ],
    [
        dash.dependencies.Input('month-selector', 'value'),
        dash.dependencies.Input('year-selector', 'value'),
    ]
)
def update_kpis(selected_month, selected_year):
    # Filter data based on selections
    monthly_data = df[(df['date'].dt.month == selected_month) & (df['date'].dt.year == selected_year)]
    annual_data = df[df['date'].dt.year == selected_year]
    previous_month = df[(df['date'].dt.month == selected_month-1) & (df['date'].dt.year == selected_year)]
    previous_year = df[df['date'].dt.year == selected_year-1]
    
    # Calculate KPIs
    monthly_revenue = monthly_data['montant_ht'].sum()
    annual_revenue = annual_data['montant_ht'].sum()
    previous_month_revenue = previous_month['montant_ht'].sum()
    previous_year_revenue = previous_year['montant_ht'].sum()
    # Assurez-vous d'abord que les revenus précédents ne sont pas nuls pour éviter la division par zéro
    if previous_month_revenue > 0:
        progress_month = (monthly_revenue / previous_month_revenue) - 1
    else:
        progress_month = 0  # ou vous pouvez choisir de le définir comme None ou un autre traitement d'erreur

    if previous_year_revenue > 0:
        progress_year = (annual_revenue / previous_year_revenue) - 1
    else:
        progress_year = 0  # ou vous pouvez choisir de le définir comme None ou un autre traitement d'erreur

    
    # Format KPIs for display
    monthly_revenue_display = f"{monthly_revenue:,.2f}€"
    annual_revenue_display = f"{annual_revenue:,.2f}€"
    progress_month_percent = "{:.2%}".format(progress_month)
    progress_year_percent = "{:.2%}".format(progress_year)
    
    return monthly_revenue_display, annual_revenue_display

# Run the app
if __name__ == '__main__':
    app.run_server(debug=False)


