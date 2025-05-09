
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

# =================== CONFIG ===================

API_KEY = 'f354a9b55fcc4ea3b5f54a423122569a'
BASE_URL = 'https://api.rawg.io/api/games'
OUTPUT_DIR = 'WP3-Output'
MAX_PAGES = 100
PAGE_SIZE = 40

# =================== HELPERS ===================

def is_steam_game(game):
    return any(store['store']['slug'] == 'steam' for store in game.get('stores', []))

def extract_game_info(game):
    return {
        'name': game.get('name'),
        'ratings_count': game.get('ratings_count', 0),
        'released': game.get('released')
    }

def fetch_games():
    all_games = []
    for page in range(1, MAX_PAGES + 1):
        print(f"📄 Lade Seite {page}...")
        params = {
            'key': API_KEY,
            'page_size': PAGE_SIZE,
            'dates': '2013-01-01,2025-12-31',
            'page': page
        }
        try:
            res = requests.get(BASE_URL, params=params)
            res.raise_for_status()
            data = res.json()
            games = data.get('results', [])
            steam_games = [extract_game_info(g) for g in games if is_steam_game(g)]
            all_games.extend(steam_games)
        except Exception as e:
            print(f"❌ Fehler beim Laden: {e}")
            break
    return pd.DataFrame(all_games)

# =================== ANALYSE ===================

def clean_and_group(df):
    df = df[(df['ratings_count'] > 0) & (df['released'].notnull())]
    df['year'] = pd.to_datetime(df['released'], errors='coerce').dt.year
    df = df[df['year'].notnull() & (df['year'] <= datetime.now().year)]
    yearly = df.groupby('year').agg(total_ratings=('ratings_count', 'sum')).reset_index()
    return yearly

def plot_time_series(df):
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='year', y='total_ratings', data=df, marker='o')
    plt.title('Anzahl Bewertungen pro Jahr (Steam-Spiele)')
    plt.xlabel('Jahr')
    plt.ylabel('Summe der Bewertungen')
    plt.grid(True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    plt.savefig(f"{OUTPUT_DIR}/ratings_over_time.png")
    plt.close()

# =================== MAIN ===================

def main():
    df = fetch_games()
    yearly_stats = clean_and_group(df)
    plot_time_series(yearly_stats)
    yearly_stats.to_csv(f"{OUTPUT_DIR}/ratings_over_time.csv", index=False)
    print("✅ Zeitreihenanalyse abgeschlossen und gespeichert.")

if __name__ == "__main__":
    main()
