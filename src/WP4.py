
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# =================== CONFIG ===================

API_KEY = 'f354a9b55fcc4ea3b5f54a423122569a'
BASE_URL = 'https://api.rawg.io/api/games'
OUTPUT_DIR = 'WP4-Output'
MAX_PAGES = 100
PAGE_SIZE = 40

# =================== HELPERS ===================

def is_steam_game(game):
    if not isinstance(game, dict):
        return False
    return any(
        isinstance(store, dict)
        and store.get('store', {}).get('slug') == 'steam'
        for store in game.get('stores', [])
    )

def extract_game_info(game):
    esrb = None
    if isinstance(game.get('esrb_rating'), dict):
        esrb = game['esrb_rating'].get('name')
    return {
        'name': game.get('name'),
        'rating': game.get('rating', None),
        'ratings_count': game.get('ratings_count', 0),
        'esrb': esrb
    }

def fetch_games():
    all_games = []
    for page in range(1, MAX_PAGES + 1):
        print(f"📄 Lade Seite {page}...")
        params = {
            'key': API_KEY,
            'page_size': PAGE_SIZE,
            'dates': '2010-01-01,2025-12-31',
            'page': page
        }
        try:
            res = requests.get(BASE_URL, params=params)
            res.raise_for_status()
            data = res.json()
            if not data or 'results' not in data:
                print(f"❌ Unerwartete API-Antwort: {data}")
                break
            games = data.get('results', [])
            steam_games = [extract_game_info(g) for g in games if g and is_steam_game(g)]
            all_games.extend(steam_games)
        except Exception as e:
            print(f"❌ Fehler beim Laden: {e}")
            break
    if not all_games:
        print("❌ Keine Spiele-Daten geladen.")
    return pd.DataFrame(all_games)

# =================== ANALYSE ===================

def analyze_esrb(df):
    required_columns = {'rating', 'ratings_count', 'esrb'}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"❌ Fehlende Spalten in DataFrame: {required_columns - set(df.columns)}")
    
    df = df[(df['rating'].notnull()) & (df['ratings_count'] > 0) & (df['esrb'].notnull()) & (df['esrb'] != 'Rating Pending')]
    summary = df.groupby('esrb').agg(
        avg_rating=('rating', 'mean'),
        median_rating=('rating', 'median'),
        game_count=('name', 'count')
    ).sort_values(by='avg_rating', ascending=False)
    return df, summary

def plot_esrb_distribution(df):
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='esrb', y='rating', data=df, palette='Set2')
    plt.title('Bewertungen nach ESRB-Kategorie')
    plt.xlabel('ESRB-Rating')
    plt.ylabel('Spielbewertung')
    plt.grid(True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    plt.savefig(f"{OUTPUT_DIR}/esrb_ratings_boxplot.png")
    plt.close()

# =================== MAIN ===================

def main():
    df = fetch_games()
    if df.empty:
        print("❌ Keine Daten zum Analysieren verfügbar.")
        return
    
    df_clean, summary = analyze_esrb(df)
    plot_esrb_distribution(df_clean)
    summary.to_csv(f"{OUTPUT_DIR}/esrb_rating_summary.csv")
    df_clean.to_csv(f"{OUTPUT_DIR}/esrb_ratings_raw.csv", index=False)
    print("✅ ESRB-Analyse abgeschlossen und gespeichert.")

if __name__ == "__main__":
    main()
