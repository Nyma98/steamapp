# 📊 Project Work SP: What Makes a Game Successful?

## 🔍 Project Overview

**Group:** 12  
**Team Members:** Kevin Lam, Nyma Dadutsang  
**Research Question:** What makes a game successful?

The goal of this project is to **analyze success factors for Steam games**. Several hypotheses were examined – e.g., whether there is a correlation between playtime and rating, whether certain genres perform better, and how ratings have changed over the years.

The data comes from the [RAWG Video Games Database API](https://rawg.io/apidocs).

---

## 🧠 Research Questions & Methods

### 1. **Correlation Between Playtime and Rating**
- **Goal:** Is there a measurable correlation?
- **Approach:** Data collected from approx. 100 Steam games including ratings and playtime.
- **Analysis:** Visualization + Pearson correlation analysis.
- **Result:** Weak but **significant positive correlation** (r ≈ 0.164, p < 0.0001).

### 2. **Top Genres by Rating**
- **Goal:** Which genres receive the highest average ratings?
- **Approach:** Analyzed 4000 games, extracted genres, calculated averages.
- **Visualization:** Bar chart of average ratings per genre.
- **Result:** For example, *Massively Multiplayer*, *Board Game*, and *Adventure* performed best.

### 3. **Development of Ratings Over the Years**
- **Goal:** How have the number and quality of ratings changed since 2015?
- **Approach:** Analyzed release dates & number of ratings.
- **Visualization:** Time series showing number & average rating per year.
- **Result:** Number of reviews per year is declining; ratings remain relatively stable.

### 4. **Impact of Age Rating (ESRB) on Game Ratings**
- **Goal:** Are games with certain age ratings rated higher?
- **Approach:** Analyzed 4000 games with ESRB data.
- **Visualization:** Bar chart per age rating.
- **Result:** *Mature* games are rated higher on average than *Everyone* games.

---

## 🗃️ Data Source & Processing

- **API:** [RAWG.io API](https://rawg.io/apidocs)
- **Pages Crawled:** 5–100 pages (depending on the question)
- **Filters:** Steam games only, released titles only, only games with ratings
- **Tools:** `requests`, `pandas`, `matplotlib`, `scipy`

CSV files were saved in several **Work Packages (WP1–WP4)**:

| Work Package | Content |
|--------------|---------|
| WP1          | Do games with a shorter playing time have lower ratings? |
| WP2          | Which genres perform best on average? |
| WP3          | How has the number of reviews for Steam games developed over the past 10 years? |
| WP4          | Is there a relationship between age rating and game rating? |

---

## 🧮 MySQL Database

### Structure (WP1):
```sql
CREATE TABLE games_wp1 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    rating FLOAT,
    playtime FLOAT,
    released DATE,
    genres TEXT
);