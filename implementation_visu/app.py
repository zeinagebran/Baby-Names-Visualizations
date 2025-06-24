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

st.session_state["NATIONAL_CSV"] = os.path.join(
    DATA_PATH, "baby_names_national.csv")
st.session_state["CLEANED_CSV"] = os.path.join(
    DATA_PATH, "baby_names_cleaned.csv")

# Page config
st.set_page_config(layout="wide", page_title="Baby Names Dashboard")

# Navigation Pages
pages = ["🏠 Home", "📈 Trends Over Time",
         "🗺️ Map by Department", "🚻 Gender Effect"]

# Handle internal page redirection from other modules
if "page_redirect" in st.session_state:
    target_page = st.session_state.page_redirect
    del st.session_state.page_redirect
    # Override radio widget using a disabled clone and force rerun
    st.sidebar.radio("Go to:", pages, index=pages.index(
        target_page), key="__page_redirect_dummy__", disabled=True)
    st.session_state.page = target_page
    st.rerun()
selected_page = st.sidebar.radio("Go to:", pages, key="page")

# Page display logic
if selected_page == "🏠 Home":
    st.title("👶 Welcome to the Baby Names Dashboard!")

    st.markdown("""
    ### Ready to explore baby names in France from 1900 to 2020?
    This dashboard lets you dive into trends, regional flavors, and gender effects on naming.

    🎉 **Have fun!** Use the navigation menu on the left to select a visualization and start your journey.
    Want to see how your favorite name evolved? Curious about regional favorites? Or the gender twist?
    It’s all just a click away!
    """)
elif selected_page == "📈 Trends Over Time":
    display_visualization_1()
elif selected_page == "🗺️ Map by Department":
    display_visualization_2()
elif selected_page == "🚻 Gender Effect":
    display_visualization_3()
