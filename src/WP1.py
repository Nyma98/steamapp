import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

# =================== CONFIG ===================

API_KEY = 'f354a9b55fcc4ea3b5f54a423122569a'
BASE_URL = 'https://api.rawg.io/api/games'
OUTPUT_DIR = 'WP1-Output'
MAX_PAGES = 5
PAGE_SIZE = 40

# =================== HELPERS ===================

def is_steam_game(game):
    return any(store['store']['slug'] == 'steam' for store in game.get('stores', []))

def extract_game_info(game):
    return {
        'name': game.get('name'),
        'playtime': game.get('playtime', 0),
        'rating': game.get('rating', None),
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
            'ordering': '-rating',
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

def analyze_playtime_vs_rating(df):
    df = df[(df['playtime'] > 0) & (df['rating'].notnull())]
    correlation = df['playtime'].corr(df['rating'])
    print(f"📊 Korrelation (Pearson) zwischen Spielzeit und Bewertung: {correlation:.2f}")
    return df, correlation

def plot_scatter(df):
    plt.figure(figsize=(10, 6))
    sns.regplot(x='playtime', y='rating', data=df, scatter_kws={'alpha':0.6})
    plt.title('Spielzeit vs. Bewertung')
    plt.xlabel('Durchschnittliche Spielzeit (h)')
    plt.ylabel('Bewertung')
    plt.grid(True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    plt.savefig(f"{OUTPUT_DIR}/playtime_vs_rating.png")
    plt.close()

# =================== MAIN ===================

def main():
    df = fetch_games()
    df_clean, corr = analyze_playtime_vs_rating(df)
    plot_scatter(df_clean)
    df_clean.to_csv(f"{OUTPUT_DIR}/playtime_vs_rating.csv", index=False)
    print("✅ Analyse abgeschlossen und gespeichert.")

if __name__ == "__main__":
    main()
