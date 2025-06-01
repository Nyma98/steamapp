import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random

# 💾 Lokalen Pfad zu deiner CSV-Datei hier einsetzen:
file_path = r"C:\Users\kevin\code\steamapp\WP4-Output\wp4_steam_esrb_ratings_20250428_203855.csv"

# CSV-Datei laden
df = pd.read_csv(file_path)

# ESRB-Kategorien auf Zahlen abbilden
unique_ratings = df['esrb_rating'].unique()
esrb_mapping = {rating: idx for idx, rating in enumerate(unique_ratings)}
df['esrb_numeric'] = df['esrb_rating'].map(esrb_mapping)

# Plot-Grundfläche
plt.figure(figsize=(14, 8))

# Farben für jede ESRB-Stufe (optional)
colors = ['blue', 'green', 'red', 'orange', 'purple', 'cyan']

# Pro ESRB-Kategorie Punkte + Trendlinie plotten
for idx, (rating, group) in enumerate(df.groupby('esrb_rating')):
    x = group['esrb_numeric'] + np.random.uniform(-0.2, 0.2, size=len(group))  # leichtes Jitter für bessere Lesbarkeit
    y = group['rating']

    # Punkte plotten
    plt.scatter(x, y, label=rating, alpha=0.6, color=colors[idx % len(colors)])

    # Regressionslinie zeichnen (nur wenn genügend Punkte vorhanden sind)
    if len(x) > 1:
        m, b = np.polyfit(x, y, 1)  # y = m*x + b
        x_fit = np.linspace(min(x), max(x), 100)
        y_fit = m * x_fit + b
        plt.plot(x_fit, y_fit, color=colors[idx % len(colors)], linestyle='--')

# Plot-Details
plt.title('Zusammenhang zwischen Altersfreigabe (ESRB) und Bewertung (Steam)')
plt.xlabel('Altersfreigabe (ESRB)')
plt.ylabel('Bewertung (0-5)')
plt.xticks(ticks=list(esrb_mapping.values()), labels=list(esrb_mapping.keys()), rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()

# Anzeigen
plt.show()
