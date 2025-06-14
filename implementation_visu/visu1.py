import streamlit as st
import pandas as pd
import plotly.express as px
import random
from utils.filters import get_top_10_names, get_sudden_changes, get_consistent_names


@st.cache_data
def load_data():
    csv_path = st.session_state["NATIONAL_CSV"]
    return pd.read_csv(csv_path)


def detect_peak_fact(name_df, name):
    peak_row = name_df.loc[name_df["births"].idxmax()]
    return f"📌 Peak popularity in {int(peak_row['year'])} with {int(peak_row['births'])} births."


def display_visualization_1():
    st.subheader("📈 Baby Name Trends in France (1900–2020)")

    st.markdown("""
        <style>
        div[data-baseweb="select"] > div > div:first-child {
            flex-wrap: wrap !important;
            max-height: 150px;
            overflow-y: auto;
        }
        </style>
    """, unsafe_allow_html=True)

    df = load_data()

    col1, col2, col3 = st.columns([3, 2, 2])

    with col2:
        gender_filter = st.radio("Gender:", ["All", "Boys", "Girls"])
    with col3:
        filter_mode = st.selectbox("🧮 Smart Filter:", [
            "None", "Top 10", "Sudden Changes", "Stable Names"])

    if gender_filter == "Boys":
        df_filtered_gender = df[df["sex"] == "M"]
    elif gender_filter == "Girls":
        df_filtered_gender = df[df["sex"] == "F"]
    else:
        df_filtered_gender = df

    if filter_mode == "Top 10":
        name_pool = get_top_10_names(df_filtered_gender)
    elif filter_mode == "Sudden Changes":
        name_pool = get_sudden_changes(df_filtered_gender)
    elif filter_mode == "Stable Names":
        name_pool = get_consistent_names(df_filtered_gender)
    else:
        name_pool = df_filtered_gender[["name", "sex"]].drop_duplicates().apply(
            tuple, axis=1).tolist()

    name_pool_key = f"{gender_filter}_{filter_mode}"

    if ("last_name_pool_key" not in st.session_state or
            st.session_state["last_name_pool_key"] != name_pool_key):
        st.session_state["last_name_pool_key"] = name_pool_key
        st.session_state["selected_names"] = random.sample(
            name_pool, min(10, len(name_pool)))

    def on_multiselect_change():
        st.session_state["selected_names"] = st.session_state["selected_names_widget"]

    def format_label(pair):
        name, sex = pair
        gender = "👦" if sex == "M" else "👧"
        return f"{name} ({gender})"

    with col1:
        selected_pairs = st.multiselect(
            label="",
            options=name_pool,
            default=st.session_state["selected_names"],
            format_func=format_label,
            key="selected_names_widget",
            label_visibility="collapsed",
            on_change=on_multiselect_change
        )

    if not selected_pairs:
        st.info("Please select one or more names from the toolbar above.")
        return

    filter_conditions = [(df["name"] == name) & (df["sex"] == sex)
                         for name, sex in selected_pairs]
    df_filtered = df[pd.concat(filter_conditions, axis=1).any(axis=1)]

    fig = px.line(
        df_filtered,
        x="year",
        y="births",
        color="name",
        line_dash="sex",
        labels={"births": "Births", "year": "Year"},
        hover_data={"births": True, "year": True, "name": True, "sex": True},
        title="Popularity Evolution of Selected Names"
    )
    fig.update_layout(height=600, legend_title="Names")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 🔍 Interesting facts")
    for name, sex in selected_pairs:
        name_df = df_filtered[(df_filtered["name"] == name)
                              & (df_filtered["sex"] == sex)]
        gender_label = "boy" if sex == "M" else "girl"
        if filter_mode == "Stable Names":
            st.markdown(
                f"**{name} ({gender_label})**: 📊 Consistently used over the years.")
        else:
            st.markdown(
                f"**{name} ({gender_label})**: {detect_peak_fact(name_df, name)}")
