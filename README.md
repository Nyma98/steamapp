# 📊 Projektarbeit SP: Was macht ein Spiel erfolgreich?

## 🔍 Projektüberblick

**Gruppe:** 12  
**Teammitglieder:** Kevin Lam, Nyma Dadutsang  
**Fragestellung:** Was macht ein Spiel erfolgreich?

Ziel dieses Projekts ist es, **Erfolgsfaktoren für Steam-Spiele** zu analysieren. Dabei wurden mehrere Hypothesen untersucht – z. B. ob es einen Zusammenhang gibt zwischen Spielzeit und Bewertung, ob bestimmte Genres besser abschneiden, und wie sich Bewertungen über die letzten Jahre verändert haben.

Die Daten stammen aus der [RAWG Video Games Database API](https://rawg.io/apidocs).

---

## 🧠 Untersuchungsfragen & Methoden

### 1. **Zusammenhang zwischen Spielzeit und Bewertung**
- **Ziel:** Gibt es einen messbaren Zusammenhang?
- **Vorgehen:** Daten von ca. 100 Steam-Spielen mit Bewertungen und Spielzeit gesammelt.
- **Analyse:** Visualisierung + Pearson-Korrelationsanalyse.
- **Ergebnis:** Schwacher, aber **signifikanter positiver Zusammenhang** (r ≈ 0.164, p < 0.0001).

### 2. **Top Genres nach Bewertung**
- **Ziel:** Welche Genres erhalten im Schnitt die besten Bewertungen?
- **Vorgehen:** 4000 Spiele analysiert, Genres extrahiert, Durchschnittswerte berechnet.
- **Visualisierung:** Balkendiagramm der Durchschnittsbewertungen je Genre.
- **Ergebnis:** z. B. *Massively Multiplayer*, *Board Game* und *Adventure* schnitten am besten ab.

### 3. **Entwicklung der Bewertungen über die Jahre**
- **Ziel:** Wie hat sich die Anzahl & Qualität der Bewertungen seit 2015 entwickelt?
- **Vorgehen:** Veröffentlichungsdaten & Anzahl Bewertungen analysiert.
- **Visualisierung:** Zeitreihe für Anzahl & durchschnittliche Bewertung je Jahr.
- **Ergebnis:** Anzahl der Reviews pro Jahr ist rückläufig; Bewertungen bleiben relativ stabil.

### 4. **Einfluss der Altersfreigabe (ESRB) auf die Bewertung**
- **Ziel:** Werden Spiele mit bestimmter Altersfreigabe besser bewertet?
- **Vorgehen:** 4000 Spiele mit ESRB-Daten analysiert.
- **Visualisierung:** Balkendiagramm pro Altersfreigabe.
- **Ergebnis:** *Mature*-Spiele schneiden durchschnittlich besser ab als *Everyone*-Spiele.

---

## 🗃️ Datenquelle & -verarbeitung

- **API:** [RAWG.io API](https://rawg.io/apidocs)
- **Seitenanzahl:** 5–100 Seiten (je nach Fragestellung)
- **Filter:** Nur Steam-Spiele, nur veröffentlichte Titel, nur Spiele mit Bewertungen
- **Tools:** `requests`, `pandas`, `matplotlib`, `scipy`

CSV-Dateien wurden in mehreren **Workpackages (WP1–WP4)** gespeichert:

| Workpackage | Inhalt |
|-------------|--------|
| WP1         | Do games with a shorter playing time have lower ratings? |
| WP2         | Which genres perform best on average? |
| WP3         | How has the number of reviews for Steam games developed over the past 10 years? |
| WP4         | s there a relationship between age rating and game rating? |

---

## 🧮 MySQL-Datenbank

### Struktur (WP1):
```sql
CREATE TABLE games_wp1 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    rating FLOAT,
    playtime FLOAT,
    released DATE,
    genres TEXT
);