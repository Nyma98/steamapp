import requests
import pandas as pd
import time
import os
from datetime import datetime
import matplotlib.pyplot as plt
import random

# Dein API Key
API_KEY = 'f354a9b55fcc4ea3b5f54a423122569a'

if not API_KEY:
    raise ValueError("❌ API Key fehlt.")

print(f"🔑 Using API Key: {API_KEY}")

BASE_URL = 'https://api.rawg.io/api/games'
games_data = []

# API-Parameter
params = {
    'key': API_KEY,
    'page_size': 40,
    'dates': '2015-01-01,2025-12-31',  # Zeitraum
}

page = 1
MAX_PAGES = 100  # ca. 4000 Spiele laden

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
        stores = game.get('stores')
        if not stores or not any(store['store']['slug'] == 'steam' for store in stores):
            continue

        released = game.get('released')
        rating = game.get('rating', None)
        esrb = game.get('esrb_rating')
        esrb_name = esrb['name'] if esrb else None  # 💥 FIX

        if not released or rating is None or esrb_name is None:
            continue

        games_data.append({
            'name': game['name'],
            'rating': rating,
            'esrb_rating': esrb_name,
            'released': released,
        })

    page += 1
    time.sleep(1)  # Schonend für die API

print(f"🎮 Gesammelte Steam-Spiele (mit Altersfreigabe): {len(games_data)}")

# Ordner für Output
output_folder = 'WP4-Output'
os.makedirs(output_folder, exist_ok=True)

# DataFrame erstellen
if games_data:
    df = pd.DataFrame(games_data)

    # CSV speichern
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = os.path.join(output_folder, f'wp4_steam_esrb_ratings_{timestamp}.csv')
    df.to_csv(filename, index=False)

    print(df.head(15))  # Vorschau
    print(f"💾 CSV gespeichert unter: {filename}")

    # Scatter-Plot vorbereiten
    plt.figure(figsize=(12, 7))

    # Für bessere Lesbarkeit: X-Achse kategorisch
    unique_ratings = df['esrb_rating'].unique()
    esrb_mapping = {rating: idx for idx, rating in enumerate(unique_ratings)}
    df['esrb_numeric'] = df['esrb_rating'].map(esrb_mapping)

    # Zufälliges Jittern, damit Punkte nicht übereinander kleben
    jitter = [random.uniform(-0.2, 0.2) for _ in range(len(df))]

    # Scatterplot zeichnen
    plt.scatter(df['esrb_numeric'] + jitter, df['rating'], alpha=0.6)
    plt.title('Zusammenhang zwischen Altersfreigabe (ESRB) und Bewertung (Steam)')
    plt.xlabel('Altersfreigabe (ESRB)')
    plt.ylabel('Bewertung (0-5)')
    plt.xticks(ticks=list(esrb_mapping.values()), labels=list(esrb_mapping.keys()), rotation=45)
    plt.grid(True)
    plt.tight_layout()

    # Plot speichern
    chart_filename = os.path.join(output_folder, f'wp4_esrb_vs_rating_{timestamp}.png')
    plt.savefig(chart_filename)
    print(f"📈 Scatter-Plot gespeichert unter: {chart_filename}")

    # Plot anzeigen
    plt.show()

else:
    print("⚠️ Keine Spiele-Daten gesammelt.")
