import os
import streamlit as st
from visu1 import display_visualization_1
from visu2 import display_visualization_2
from visu3 import display_visualization_3

# Paths
if os.path.exists("data/baby_names_national.csv"):
    DATA_PATH = "data"
else:
    DATA_PATH = "implementation_visu/data"

st.session_state["NATIONAL_CSV"] = os.path.join(DATA_PATH, "baby_names_national.csv")
st.session_state["CLEANED_CSV"] = os.path.join(DATA_PATH, "baby_names_cleaned.csv")

# Page config
st.set_page_config(layout="wide", page_title="Baby Names Dashboard")

# Navigation Pages
pages = ["🏠 Home", "📈 Trends Over Time", "🗺️ Map by Department", "🚻 Gender Effect"]

# Only set default the first time
if "active_page" not in st.session_state:
    st.session_state.active_page = pages[0]

# Handle internal page redirection from other modules
if "page_redirect" in st.session_state:
    st.session_state.active_page = st.session_state.page_redirect
    del st.session_state.page_redirect
    st.rerun()

# Sidebar navigation
selected = st.sidebar.radio("Go to:", pages, index=pages.index(st.session_state.active_page), key="nav_radio")
st.session_state.active_page = selected

# Page display logic
if st.session_state.active_page == "🏠 Home":
    st.title("👶 Welcome to the Baby Names Dashboard!")

    st.markdown("""
    ### Ready to explore baby names in France from 1900 to 2020?
    This dashboard lets you dive into trends, regional flavors, and gender effects on naming.

    🎉 **Have fun!** Use the navigation menu on the left to select a visualization and start your journey.
    Want to see how your favorite name evolved? Curious about regional favorites? Or the gender twist?
    It’s all just a click away!
    """)
elif st.session_state.active_page == "📈 Trends Over Time":
    display_visualization_1()
elif st.session_state.active_page == "🗺️ Map by Department":
    display_visualization_2()
elif st.session_state.active_page == "🚻 Gender Effect":
    display_visualization_3()
