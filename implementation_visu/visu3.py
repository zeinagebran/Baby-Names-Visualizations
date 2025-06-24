import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

color = {"M": "#1f77b4", "F": "#e91e63"}
FILL = {
    k: f"rgba({int(c[1:3], 16)}, {int(c[3:5], 16)}, {int(c[5:7], 16)},0.4)" for k, c in color.items()}


@st.cache_data
def load_data():
    csv_path = st.session_state["NATIONAL_CSV"]
    return pd.read_csv(csv_path)


def peaknote(df):
    row = df.loc[df["births"].idxmax()]
    return f"📌 Peak in {int(row.year)}: {int(row.births)} births ({'girls' if row.sex == 'F' else 'boys'})"


def styled_caption(text):
    st.markdown(f"<div style='margin-top: -15px; color: gray; font-size: 0.85em'>{text}</div>",
                unsafe_allow_html=True)


def plot_multi_year(name, name_df):
    fig = go.Figure()
    years_unique = name_df["year"].nunique()
    for sex in name_df["sex"].unique():
        df_sex = name_df[name_df["sex"] == sex]
        if years_unique == 1:
            row = df_sex.iloc[0]
            fig.add_trace(go.Scatter(
                x=[row["year"], row["year"]],
                y=[0, row["births"]],
                mode="lines",
                line=dict(color=FILL[sex], width=2),
                name=sex,
                showlegend=True))
            fig.add_trace(go.Scatter(
                x=[row["year"]],
                y=[row["births"]],
                mode="markers",
                marker=dict(size=6, color=FILL[sex]),
                name="",
                showlegend=False))
        else:
            fig.add_trace(go.Scatter(
                x=df_sex["year"],
                y=df_sex["births"],
                mode="lines+markers",
                marker=dict(size=2, color=color[sex], opacity=0.2),
                line=dict(color=color[sex], width=1.5),
                fill="tozeroy",
                fillcolor=FILL.get(sex),
                name=sex,
                showlegend=True))
    fig.update_layout(
        title=name,
        height=400,
        legend_title="Gender",
        yaxis_title="Births")
    if years_unique == 1:
        year = name_df["year"].iloc[0]
        fig.update_layout(xaxis=dict(tickmode='array', tickvals=[year]))

    return fig


def main_charts(name_dict, names):
    if not names:
        df = load_data()
        area_df = df.groupby(["year", "sex"])["births"].sum().reset_index()
        fig = go.Figure()
        for sex in ["F", "M"]:
            sub_df = area_df[area_df["sex"] == sex]
            fig.add_trace(go.Scatter(x=sub_df["year"], y=sub_df["births"],
                                     mode="lines", name=sex,
                                     line=dict(shape="spline",
                                               width=2, color=color[sex]),
                                     fill="tozeroy", fillcolor=FILL[sex]))
        fig.update_layout(title="Overall Birth Trends by Gender",
                          xaxis_title="Year", yaxis_title="Births",
                          legend_title="Gender",
                          height=400, hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)
        return

    num = len(names)
    cols = st.columns(min(num, 3))
    for i, name in enumerate(names):
        df_raw = name_dict.get(name)
        if df_raw is None or df_raw.empty:
            continue
        df = df_raw[df_raw["births"] > 0]
        if df.empty:
            st.warning(f"⚠️ No data to display for **{name}**.")
            continue

        with cols[i % len(cols)]:
            fig = plot_multi_year(name, df)
            st.plotly_chart(fig, use_container_width=True)
            styled_caption(peaknote(df))


def get_smart_filter_names(df, top_n=10):
    grouped = df.groupby(["name", "sex"])["births"].sum().unstack().fillna(0)
    grouped["total"] = grouped["M"] + grouped["F"]
    grouped["min_count"] = grouped[["M", "F"]].min(axis=1)

    filtered = grouped[(grouped["M"] >= 1000) & (grouped["F"] >= 1000)].copy()
    filtered["ratio_diff"] = abs(filtered["M"] / filtered["total"] - 0.5)
    top_unisex = (filtered.sort_values(["ratio_diff", "total"], ascending=[True, False])
                  .head(top_n).index.tolist())

    top_boys = grouped[grouped["M"] > 0].sort_values(
        "M", ascending=False).head(top_n).index.tolist()
    top_girls = grouped[grouped["F"] > 0].sort_values(
        "F", ascending=False).head(top_n).index.tolist()

    return top_boys, top_girls, top_unisex


def display_visualization_3():
    st.subheader("🚻 Baby Name Gender Effect in France (1900-2020)")

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

    # Initialize session state cleanly
    st.session_state.setdefault("selected_names3_input", [])
    st.session_state.setdefault("smart_choice", "None")
    st.session_state.setdefault("top_n", 10)

    # Load or cache name dictionary
    if "name_dict" not in st.session_state:
        st.session_state["name_dict"] = {
            n: g.reset_index(drop=True) for n, g in df.groupby("name")
        }
    name_dict = st.session_state["name_dict"]

    # Handle navigation from Visu1
    preselect = st.session_state.pop("selected_name_for_visu3", None)
    if preselect:
        if isinstance(preselect, str):
            preselect = [preselect]
        st.session_state["smart_choice"] = "None"
        st.session_state["selected_names3_input"] = list(set(preselect))

    name_pool = sorted(df["name"].unique())

    smart_options = [
        "None",
        "👦 Most Popular Boy Names",
        "👧 Most Popular Girl Names",
        "🚻 Most Gender-Neutral Names"
    ]

    smart_choice = st.selectbox(
        "🧮 Smart filter:",
        smart_options,
        index=smart_options.index(st.session_state["smart_choice"])
    )

    # Smart filter applied
    if smart_choice != "None":
        top_n = st.slider(
            "Select number of names to display in Smart Filter",
            min_value=5,
            max_value=30,
            value=st.session_state["top_n"]
        )

        top_boys, top_girls, top_unisex = get_smart_filter_names(df, top_n)

        if (
            smart_choice != st.session_state["smart_choice"]
            or top_n != st.session_state["top_n"]
        ):
            st.session_state["smart_choice"] = smart_choice
            st.session_state["top_n"] = top_n

            if smart_choice == "👦 Most Popular Boy Names":
                suggestions = top_boys[:top_n]
            elif smart_choice == "👧 Most Popular Girl Names":
                suggestions = top_girls[:top_n]
            elif smart_choice == "🚻 Most Gender-Neutral Names":
                suggestions = top_unisex[:top_n]
            else:
                suggestions = []

            st.session_state["smart_suggestions"] = suggestions
            st.session_state["selected_names3_input"] = suggestions
            st.rerun()

    # Main name selection widget
    selected = st.multiselect(
        " ",
        name_pool,
        key="selected_names3_input",
        placeholder="Choose names",
        label_visibility="collapsed"
    )

    # Reset smart filter if manual selection diverges
    if st.session_state["smart_choice"] != "None":
        valid = st.session_state.get("smart_suggestions", [])
        if any(name not in valid for name in selected):
            st.session_state["smart_choice"] = "None"
            st.rerun()

    # Reset if list is cleared
    if not selected and st.session_state["smart_choice"] != "None":
        st.session_state["smart_choice"] = "None"
        st.session_state["top_n"] = 10
        st.rerun()

    # Adjust top_n down if fewer results remain
    if st.session_state["smart_choice"] != "None":
        if len(st.session_state["selected_names3_input"]) < st.session_state["top_n"]:
            st.session_state["top_n"] = len(
                st.session_state["selected_names3_input"])
            st.rerun()

    # Render main charts
    main_charts(name_dict, selected)
