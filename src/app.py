import os
import pandas as pd
import dash
from dash import html, dcc
import plotly.express as px

def safe_read_csv(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    else:
        print(f"Datei nicht gefunden: {path}")
        return pd.DataFrame()

# Passe die Dateinamen ggf. an die aktuellen CSVs an!
df_wp1 = safe_read_csv('../WP1-Output/.ipynb_checkpoints/"wp1_steam_games_20250422_204305-checkpoint.csv')
df_wp2 = safe_read_csv('../WP2-Output/steam_genre_average_20250509_224132.csv')
df_wp3 = safe_read_csv('../WP3-Output/wp3_steam_ratings_20250509_224311.csv')
df_wp4 = safe_read_csv('../WP4-Output/wp4_steam_esrb_ratings_20250509_224627.csv')

app = dash.Dash(__name__)
app.title = "🎮 Steam Games Analyse"

app.layout = html.Div([
    html.H1("📊 Analyse: Was macht ein Spiel erfolgreich?", style={'textAlign': 'center'}),

    html.H2("1️⃣ Spielzeit vs Bewertung"),
    dcc.Graph(
        figure=px.scatter(
            df_wp1[df_wp1["playtime"] > 0] if "playtime" in df_wp1.columns and "rating" in df_wp1.columns else pd.DataFrame(),
            x="playtime" if "playtime" in df_wp1.columns else None,
            y="rating" if "rating" in df_wp1.columns else None,
            hover_name="name" if "name" in df_wp1.columns else None,
            title="Spielzeit vs Bewertung (Steam)",
            trendline="ols"
        )
    ) if not df_wp1.empty else html.Div("Keine Daten für Spielzeit vs Bewertung verfügbar."),

    html.H2("2️⃣ Durchschnittsbewertung pro Genre"),
    dcc.Graph(
        figure=px.bar(
            df_wp2.sort_values("rating", ascending=True) if "rating" in df_wp2.columns and "genre" in df_wp2.columns else pd.DataFrame(),
            x="rating" if "rating" in df_wp2.columns else None,
            y="genre" if "genre" in df_wp2.columns else None,
            orientation='h',
            title="Top Genres nach Bewertung",
            labels={'rating': 'Durchschnittliche Bewertung', 'genre': 'Genre'}
        )
    ) if not df_wp2.empty else html.Div("Keine Daten für Durchschnittsbewertung pro Genre verfügbar."),

    html.H2("3️⃣ Bewertungen über die Jahre (2015–2025)"),
    dcc.Graph(
        figure=px.line(
            df_wp3.assign(year=pd.to_datetime(df_wp3['released']).dt.year)
                    .groupby('year')['ratings_count'].sum().reset_index() if 'released' in df_wp3.columns and 'ratings_count' in df_wp3.columns else pd.DataFrame(),
            x="year" if 'released' in df_wp3.columns else None,
            y="ratings_count" if 'ratings_count' in df_wp3.columns else None,
            markers=True,
            title="Gesamtanzahl Bewertungen pro Jahr"
        )
    ) if not df_wp3.empty else html.Div("Keine Daten für Bewertungen über die Jahre verfügbar."),

    html.H2("4️⃣ Bewertung nach Altersfreigabe (ESRB)"),
    dcc.Graph(
        figure=px.bar(
            df_wp4[df_wp4['esrb_rating'].isin(['Everyone', 'Teen', 'Mature', 'Adults Only'])] if 'esrb_rating' in df_wp4.columns and 'rating' in df_wp4.columns else pd.DataFrame()
                    .groupby("esrb_rating")["rating"].mean().reset_index() if 'esrb_rating' in df_wp4.columns and 'rating' in df_wp4.columns else pd.DataFrame(),
            x="esrb_rating" if 'esrb_rating' in df_wp4.columns else None,
            y="rating" if 'rating' in df_wp4.columns else None,
            title="Durchschnittliche Bewertung nach ESRB",
            labels={'rating': 'Bewertung', 'esrb_rating': 'Altersfreigabe'}
        )
    ) if not df_wp4.empty else html.Div("Keine Daten für Bewertung nach Altersfreigabe verfügbar."),

    html.Footer("Projektarbeit Gruppe 12 – Kevin Lam & Nyma Dadutsang", style={'textAlign': 'center', 'marginTop': '50px'})
])

if __name__ == "__main__":
    app.run(debug=True)