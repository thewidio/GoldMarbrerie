# Importation des bibliothèques nécessaires
import dash
from dash import dcc
from dash import html
from sqlalchemy import create_engine
import pandas as pd
import plotly.express as px
import os


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

    # KPI's Titre
    html.H2('Principaux indicateurs', style={'textAlign': 'left'}),

    # KPIs Display
    html.Div([
        # KPI Box for Monthly Sales
        html.Div([
            html.Div([
                html.Div('Ventes mensuelles', className='kpi-title'),
                html.Div(id='progress_month', className='kpi-calculation')
            ], style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center'}),
            html.Div(id='monthly-revenue', className='kpi-value'),
            html.Div('Mois en cours par rapport au mois précédent', className='kpi-description')
        ], className='kpi-box'),

        # KPI Box for Annual Sales
        html.Div([
            html.Div([
                html.Div('Ventes annuelles', className='kpi-title'),
                html.Div(id='progress_year', className='kpi-calculation')
            ], style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center'}),
            html.Div(id='annual-revenue', className='kpi-value'),
            html.Div("Année en cours par rapport à l'année précédente", className='kpi-description')
        ], className='kpi-box'),

        # KPI Box for Cumulated Sales
        html.Div([
            html.Div([
                html.Div('Ventes cumulées', className='kpi-title'),
                html.Div(id='progress_cumulated', className='kpi-calculation')
            ], style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center'}),
            html.Div(id='cumulated_revenue', className='kpi-value'),
            html.Div("Depuis le début de l'année", className='kpi-description')
        ], className='kpi-box'),
    ], style={'display': 'flex', 'justifyContent': 'space-around'}),

    # Ajout du titre et de l'espace pour l'histogramme
    html.Div([
        html.H2("Ventes Mensuelles", style={'textAlign': 'left'}),
        dcc.Graph(id='monthly-sales-histogram'),  # Cet élément dcc.Graph va contenir l'histogramme
    ], style={'width': '100%', 'display': 'inline-block'})
])

# Callbacks to update KPIs
@app.callback(
    [
        dash.dependencies.Output('monthly-revenue', 'children'),
        dash.dependencies.Output('annual-revenue', 'children'),
        dash.dependencies.Output('progress_month', 'children'),
        dash.dependencies.Output('progress_year', 'children'),
        dash.dependencies.Output('cumulated_revenue', 'children'),
        dash.dependencies.Output('progress_cumulated', 'children'),
        dash.dependencies.Output('monthly-sales-histogram', 'figure'),
    ],
    [
        dash.dependencies.Input('month-selector', 'value'),
        dash.dependencies.Input('year-selector', 'value'),
    ]
)

def update_kpis_and_histogram(selected_month, selected_year):
    # Filter data based on selections
    monthly_data = df[(df['date'].dt.month == selected_month) & (df['date'].dt.year == selected_year)]
    annual_data = df[df['date'].dt.year == selected_year]
    cumulated_data = df[(df['date'].dt.month <= selected_month) & (df['date'].dt.year == selected_year)]
    previous_month_data = df[(df['date'].dt.month == selected_month-1) & (df['date'].dt.year == selected_year)]
    previous_year_data = df[df['date'].dt.year == selected_year-1]
    previous_cumulated_data = df[(df['date'].dt.month <= selected_month) & (df['date'].dt.year == selected_year-1)]
    
    # Calculate KPIs
    monthly_revenue = monthly_data['montant_ht'].sum()
    annual_revenue = annual_data['montant_ht'].sum()
    cumulated_revenue = cumulated_data['montant_ht'].sum()
    print(cumulated_revenue)
    previous_month_revenue = previous_month_data['montant_ht'].sum()
    previous_year_revenue = previous_year_data['montant_ht'].sum()
    previous_cumulated_revenue = previous_cumulated_data['montant_ht'].sum()

    # Assurez-vous d'abord que les revenus précédents ne sont pas nuls pour éviter la division par zéro
    if previous_month_revenue > 0:
        progress_month = (monthly_revenue / previous_month_revenue) - 1
    else:
        progress_month = 0  # ou vous pouvez choisir de le définir comme None ou un autre traitement d'erreur

    if previous_year_revenue > 0:
        progress_year = (annual_revenue / previous_year_revenue) - 1
    else:
        progress_year = 0  # ou vous pouvez choisir de le définir comme None ou un autre traitement d'erreur
    if previous_cumulated_revenue > 0:
        progress_cumulated = (cumulated_revenue / previous_cumulated_revenue) - 1
    else:
        progress_cumulated = 0
    
    
    # Format KPIs for display
    monthly_revenue_display = f"{monthly_revenue:,.0f}€".replace(',', ' ')
    annual_revenue_display = f"{annual_revenue:,.0f}€".replace(',', ' ')
    cumulated_revenue_display = f"{cumulated_revenue:,.0f}€".replace(',', ' ')
    progress_month_percent = "{:.1%}".format(progress_month).replace(',', ' ')
    progress_year_percent = "{:.1%}".format(progress_year).replace(',', ' ')
    progress_cumulated_percent = "{:.1%}".format(progress_cumulated).replace(',', ' ')
    
# Logique pour créer l'histogramme
    filtered_data = df[(df['date'].dt.month <= selected_month) & (df['date'].dt.year == selected_year)]
    monthly_sales = filtered_data.groupby(filtered_data['date'].dt.month)['montant_ht'].sum().reset_index()
    fig = px.bar(
        monthly_sales,
        x='date',  # Assurez-vous que cette colonne contient les mois
        y='montant_ht',  # Cette colonne doit contenir le total des ventes
        labels={'date': 'Mois', 'montant_ht': 'Ventes (€)'},
        title=f'Ventes Mensuelles pour {selected_year}'
    )    

    return (monthly_revenue_display, annual_revenue_display, 
            progress_month_percent, progress_year_percent, 
            cumulated_revenue_display, progress_cumulated_percent, fig.to_dict())




# Run the app
if __name__ == '__main__':
    # Get the PORT from the environment variable (if not found, default to 8050)
    port = int(os.environ.get('PORT', 8050))
    # Run the server on all available interfaces and the port specified by Render
    app.run_server(host='0.0.0.0', port=port)

