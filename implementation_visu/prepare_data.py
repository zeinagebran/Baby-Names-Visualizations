import streamlit as st
from visu1 import display_visualization_1
# from visu2 import display_visualization_2
# from visu3 import display_visualization_3
import os

# Dynamically detect correct data path
if os.path.exists("data/baby_names_national.csv"):
    DATA_PATH = "data"
else:
    DATA_PATH = "implementation_visu/data"

# Store paths in session state for other modules
st.session_state["NATIONAL_CSV"] = os.path.join(DATA_PATH, "baby_names_national.csv")
st.session_state["CLEANED_CSV"] = os.path.join(DATA_PATH, "baby_names_cleaned.csv")

st.set_page_config(layout="wide", page_title="Baby Names Dashboard")

st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio("Go to:", [
    "🏠 Home",
    "📈 Trends Over Time",
    "🗺️ Map by Department",
    "🚻 Gender Effect"
])

if page == "🏠 Home":
    st.title("Welcome to the Baby Names Dashboard")
    st.markdown("""
    ### Explore baby name trends in France (1900–2020)

    Navigate through different views using the sidebar to analyze name popularity over time,
    regional distribution, and gender-based patterns.
    """)
elif page == "📈 Trends Over Time":
    display_visualization_1()
elif page == "🗺️ Map by Department":
    display_visualization_2()
elif page == "🚻 Gender Effect":
    display_visualization_3()
