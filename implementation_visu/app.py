import streamlit as st
from visu1 import display_visualization_1
# from visu2 import display_visualization_2
# from visu3 import display_visualization_3

st.set_page_config(layout="wide", page_title="Baby Names Dashboard")

st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio("Go to:", [
    "🏠 Home",
    "📈 Trends Over Time",
    "🗺️ Map by Department",
    "🚻 Gender Effect"
])

if page == "🏠 Home":
    st.title("👶 Welcome to the Baby Names Dashboard!")
    st.markdown("""
    ### Ready to explore baby names in France from 1900 to 2020?
    This dashboard lets you dive into trends, regional flavors, and gender effects on naming.

    🎉 **Have fun!** Use the navigation menu on the left to select a visualization and start your journey.
    Want to see how your favorite name evolved? Curious about regional favorites? Or the gender twist?
    It’s all just a click away!
    """)
elif page == "📈 Trends Over Time":
    display_visualization_1()
elif page == "🗺️ Map by Department":
    display_visualization_2()
elif page == "🚻 Gender Effect":
    display_visualization_3()
