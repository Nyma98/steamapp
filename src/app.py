import pandas as pd
import dash
from dash import html, dcc
import plotly.express as px

# CSV-Dateien laden (Passe Pfade ggf. an)
df_wp1 = pd.read_csv('WP1-Output/steam_games_20250509_223849.csv')
df_wp2 = pd.read_csv('WP2-Output/steam_genre_average_20250509_224132.csv')
df_wp3 = pd.read_csv('WP3-Output/wp3_steam_ratings_20250509_224311.csv')
df_wp4 = pd.read_csv('WP4-Output/wp4_steam_esrb_ratings_20250509_224627.csv')

# App-Initialisierung
app = dash.Dash(__name__)
app.title = "🎮 Steam Games Analyse"

# Layout
app.layout = html.Div([
    html.H1("📊 Analyse: Was macht ein Spiel erfolgreich?", style={'textAlign': 'center'}),

    html.H2("1️⃣ Spielzeit vs Bewertung"),
    dcc.Graph(
        figure=px.scatter(
            df_wp1[df_wp1["playtime"] > 0],
            x="playtime",
            y="rating",
            hover_name="name",
            title="Spielzeit vs Bewertung (Steam)",
            trendline="ols"
        )
    ),

    html.H2("2️⃣ Durchschnittsbewertung pro Genre"),
    dcc.Graph(
        figure=px.bar(
            df_wp2.sort_values("rating", ascending=True),
            x="rating",
            y="genre",
            orientation='h',
            title="Top Genres nach Bewertung",
            labels={'rating': 'Durchschnittliche Bewertung', 'genre': 'Genre'}
        )
    ),

    html.H2("3️⃣ Bewertungen über die Jahre (2015–2025)"),
    dcc.Graph(
        figure=px.line(
            df_wp3.assign(year=pd.to_datetime(df_wp3['released']).dt.year)
                    .groupby('year')['ratings_count'].sum().reset_index(),
            x="year",
            y="ratings_count",
            markers=True,
            title="Gesamtanzahl Bewertungen pro Jahr"
        )
    ),

    html.H2("4️⃣ Bewertung nach Altersfreigabe (ESRB)"),
    dcc.Graph(
        figure=px.bar(
            df_wp4[df_wp4['esrb_rating'].isin(['Everyone', 'Teen', 'Mature', 'Adults Only'])]
                    .groupby("esrb_rating")["rating"].mean().reset_index(),
            x="esrb_rating",
            y="rating",
            title="Durchschnittliche Bewertung nach ESRB",
            labels={'rating': 'Bewertung', 'esrb_rating': 'Altersfreigabe'}
        )
    ),

    html.Footer("Projektarbeit Gruppe 12 – Kevin Lam & Nyma Dadutsang", style={'textAlign': 'center', 'marginTop': '50px'})
])