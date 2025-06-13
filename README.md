## Baby Names Dashboard – France (1900–2020)

**App link** → 🌐 [https://baby-names-visualizations-gebranzeina.streamlit.app/](https://baby-names-visualizations-gebranzeina.streamlit.app/)

**Objective**  
The **Baby Names Dashboard – France** is an interactive application that enables exploration of baby name trends across France from 1900 to 2020. Designed for decision-makers, analysts, and curious users, the tool provides powerful filtering, visualization, and insights into historical naming patterns.

---

## 🚀 Features and Visualizations

**1. Trends Over Time**  
Visual 1 provides a clear temporal analysis of baby name popularity in France:
- Filter by gender (Boys / Girls / All)
- Apply smart filters: Top 10, Significant Changes, or Stable Names
- Compare multiple names over time
- View metrics like peak popularity year and number of births

**2. Map by Department** *(coming soon)*  
A regional heatmap to explore:
- Most popular names by department
- Gender and year filters
- Regional comparisons and anomalies

**3. Gender Effect** *(coming soon)*  
Insights into how names evolve across genders:
- Male vs Female name trends
- Identify unisex names
- Contrast naming habits over decades

---

## 🧹 Data Preprocessing

We start from the raw file `dpt2020.csv` and perform several cleaning steps:
- Remove rare or anonymized entries (`_PRENOMS_RARES`, `XXXX` years)
- Convert columns into clean formats: `name`, `year`, `sex`, `dept`, `births`
- Normalize department codes (e.g., “1” → “01”)

From this process, two ready-to-use datasets are generated:
- `baby_names_cleaned.csv` → includes department and gender, for geographic and demographic visuals
- `baby_names_national.csv` → aggregated view across France, used for trend visualization

Filter utilities are modularized under `utils/filters.py` and used across the app logic.

---

## 💻 How to Run the Project Locally

```bash
# 1. Clone the repository
git clone https://github.com/zeinagebran/Baby-Names-Visualizations.git

# 2. Move into the project folder
cd Baby-Names-Visualizations

# 3. Launch the Streamlit app
streamlit run "implementation_visu/app.py"
