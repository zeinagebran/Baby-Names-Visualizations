## Baby Names Dashboard – France (1900–2020)

**Objective**  
This dashboard provides an interactive exploration of baby name trends in France from 1900 to 2020. It is designed for decision-makers, data analysts, and the general public seeking insights into name popularity, regional dynamics, and gender-based naming patterns.

---

## Features and Visualizations

**1. Trends Over Time**  
*Visual 1* offers a clean temporal analysis of baby name popularity across France.  
- Filter by gender  
- Explore top 10 names, names with significant shifts, or stable trends  
- Compare multiple names simultaneously  
- Gain insights such as peak popularity year and birth counts

**2. Map by Department** *(coming soon)*  
*Visual 2* will display a geographical heatmap of name popularity by French department.  
- Filter by gender and year  
- Highlight the most popular names regionally

**3. Gender Effect** *(coming soon)*  
*Visual 3* will focus on how naming choices vary across genders.  
- Compare popularity curves  
- Explore unisex trends and strong gender splits

---

## Data Preprocessing

The project begins with a raw dataset of baby names in France (`dpt2020.csv`), which is thoroughly cleaned and transformed for analysis:

- Rare and invalid entries (`_PRENOMS_RARES`, unknown years) are filtered out  
- Columns are renamed and cast to appropriate types (`name`, `year`, `sex`, `dept`, `births`)  
- Department codes are standardized using two-digit formatting

Two datasets are generated and saved in the `data/` directory:

- `baby_names_cleaned.csv`: cleaned data with full granularity (department + gender)
- `baby_names_national.csv`: national-level aggregation, used for trend visualizations

Utility filters (e.g. top 10, sudden changes, consistent names) are implemented in `utils/filters.py` and integrated directly into the app logic.

---
## How to Run the Project

```bash
# 1. Clone the repository
git clone https://github.com/zeinagebran/Baby-Names-Visualizations.git

# 2. Launch the dashboard
streamlit run "implementation visu/app.py"

```
