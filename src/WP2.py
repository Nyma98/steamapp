
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# =================== CONFIG ===================

API_KEY = 'f354a9b55fcc4ea3b5f54a423122569a'
BASE_URL = 'https://api.rawg.io/api/games'
OUTPUT_DIR = 'WP2-Output'
MAX_PAGES = 100
PAGE_SIZE = 40
MIN_RATINGS = 10

# =================== HELPERS ===================

def is_steam_game(game):
    return any(store['store']['slug'] == 'steam' for store in game.get('stores', []))

def extract_game_info(game):
    return {
        'name': game.get('name'),
        'genres': [g['name'] for g in game.get('genres', [])],
        'rating': game.get('rating'),
        'ratings_count': game.get('ratings_count'),
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

def explode_genres(df):
    df = df[df['genres'].map(len) > 0]  # Entferne Spiele ohne Genre
    df = df.explode('genres')
    return df

def analyze_genres(df):
    df = df[(df['rating'].notnull()) & (df['ratings_count'] >= MIN_RATINGS) & (df['rating'] >= 4.0) & (df['rating'] <= 5.0)]
    df = explode_genres(df)
    genre_stats = df.groupby('genres').agg(
        avg_rating=('rating', 'mean'),
        game_count=('name', 'count')
    ).sort_values(by='avg_rating', ascending=False)
    return genre_stats

def plot_top_genres(genre_stats, top_n=10):
    top = genre_stats.head(top_n).sort_values(by='avg_rating')
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top['avg_rating'], y=top.index, palette='viridis')
    plt.title(f'Top {top_n} Genres nach Bewertung')
    plt.xlabel('Durchschnittliche Bewertung')
    plt.ylabel('Genre')
    plt.grid(True, axis='x')
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    plt.savefig(f"{OUTPUT_DIR}/top_genres.png")
    plt.close()

# =================== MAIN ===================

def main():
    df = fetch_games()
    genre_stats = analyze_genres(df)
    plot_top_genres(genre_stats)
    genre_stats.to_csv(f"{OUTPUT_DIR}/genre_ratings.csv")
    print("✅ Analyse abgeschlossen und gespeichert.")

if __name__ == "__main__":
    main()
