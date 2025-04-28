import requests
import pandas as pd
import time
from datetime import datetime
import os
import matplotlib.pyplot as plt

# Dein API Key
API_KEY = 'f354a9b55fcc4ea3b5f54a423122569a'

if not API_KEY:
    raise ValueError("❌ API Key fehlt.")

print(f"🔑 Using API Key: {API_KEY}")

BASE_URL = 'https://api.rawg.io/api/games'
games_data = []

# Parameter
params = {
    'key': API_KEY,
    'page_size': 40,
    'ordering': '-rating'
}

page = 1
MAX_PAGES = 100  # 100 Seiten x 40 Spiele = 4000 Spiele

while page <= MAX_PAGES:
    params['page'] = page
    print(f"📄 Lade Seite {page}...")

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Fehler beim Abrufen: {e}")
        break

    if 'results' not in data or not data['results']:
        print("✅ Keine weiteren Ergebnisse.")
        break

    for game in data['results']:
        # Prüfe, ob auf Steam verfügbar
        if not any(store['store']['slug'] == 'steam' for store in game.get('stores', [])):
            continue

        games_data.append({
            'name': game['name'],
            'rating': game['rating'],
            'ratings_count': game['ratings_count'],
            'playtime': game['playtime'],
            'released': game['released'],
            'genres': [genre['name'] for genre in game['genres']],
        })

    page += 1
    time.sleep(1)  # API nicht überlasten

print(f"🎮 Gesammelte Steam-Spiele: {len(games_data)}")

# DataFrame & Speichern
if games_data:
    df = pd.DataFrame(games_data)
    print(df.head())

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Ordner für Output erstellen
    output_folder = 'WP2-Output'
    os.makedirs(output_folder, exist_ok=True)

    filename = os.path.join(output_folder, f'steam_games_{timestamp}.csv')
    df.to_csv(filename, index=False)

    full_path = os.path.abspath(filename)
    print(f"💾 Rohdaten gespeichert unter: {full_path}")

    # --- Zusätzliche Auswertung für WP2 ---
    genre_ratings = []

    for idx, row in df.iterrows():
        for genre in row['genres']:
            genre_ratings.append({
                'genre': genre,
                'rating': row['rating']
            })

    genre_df = pd.DataFrame(genre_ratings)

    # Durchschnittliche Bewertung pro Genre berechnen
    genre_avg = genre_df.groupby('genre').mean().reset_index()
    genre_avg = genre_avg.sort_values(by='rating', ascending=False)

    genre_filename = os.path.join(output_folder, f'steam_genre_average_{timestamp}.csv')
    genre_avg.to_csv(genre_filename, index=False)

    genre_full_path = os.path.abspath(genre_filename)
    print(f"💾 Genre-Durchschnitt gespeichert unter: {genre_full_path}")

    # Ausgabe der besten Genres
    print("\n🏆 Top Genres nach durchschnittlicher Bewertung:")
    print(genre_avg.head(10))

    # --- Diagramm erstellen ---
    plt.figure(figsize=(12, 8))
    plt.barh(genre_avg['genre'][:10][::-1], genre_avg['rating'][:10][::-1])
    plt.xlabel('Durchschnittliche Bewertung')
    plt.ylabel('Genre')
    plt.title('Top 10 Genres nach Durchschnittsbewertung')
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()

    # Diagramm speichern
    diagram_filename = os.path.join(output_folder, f'top10_genre_plot_{timestamp}.png')
    plt.savefig(diagram_filename)
    print(f"🖼️ Diagramm gespeichert unter: {os.path.abspath(diagram_filename)}")

    # Diagramm anzeigen
    plt.show()

else:
    print("⚠️ Keine Spiele-Daten gesammelt.")
