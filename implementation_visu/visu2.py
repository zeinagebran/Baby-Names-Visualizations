import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import json
import shapely.geometry as geom
from wordcloud import WordCloud
from io import BytesIO
import base64


@st.cache_data
def load_geojson():
    with open("implementation_visu/data/departments.geojson", "r", encoding="utf-8") as f:
        return json.load(f)


def make_wordcloud_base64(word_freqs, width=180, height=100, padding_factor=0.75, max_font=80):
    width = int(width * padding_factor)
    height = int(height * padding_factor)

    wc = WordCloud(
        width=width,
        height=height,
        background_color=None,
        mode="RGBA",
        colormap="tab10",
        prefer_horizontal=1.0,
        min_font_size=4,
        max_font_size=max_font,
        max_words=10
    ).generate_from_frequencies(word_freqs)

    img = wc.to_image()
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()


def display_visualization_2():
    st.subheader("🗺️ Most Popular Baby Names by Department (2020)")

    # --- at top of your display_visualization_2(), before `df = pd.read_csv(…)` ---



    # 🔧 Handle dynamic input from Visu1
    selected_name = st.session_state.pop("selected_name_for_visu2", None)

    if selected_name is None:
        st.info("Each department shows a word cloud of its top 5 names.")
    else:
        st.success(f"Showing regional popularity for **{selected_name}**")

    topN = 5

    df = pd.read_csv(st.session_state["CLEANED_CSV"])

    
    min_year, max_year = int(df["year"].min()), int(df["year"].max())

    if 'year' not in st.session_state:
        st.session_state.year = 2020  

    spacer_l, col_left, col_center, col_right, spacer_r = st.columns([1, 1, 6, 1, 1])

    with col_left:
        if st.button("←"):
            st.session_state.year = max(min_year, st.session_state.year - 1)

    with col_center:
       
        inner_l, inner_mid, inner_r = st.columns([1, 2, 1])

        with inner_mid:
            year_str = st.text_input(
                "", 
                value=str(st.session_state.year),
                max_chars=4,
                key="year_text",
                label_visibility="collapsed"  
            )
          
            if year_str.isdigit():
                y = int(year_str)
                if min_year <= y <= max_year:
                    st.session_state.year = y
                else:
                    st.error(f"Year must be between {min_year} and {max_year}")
            else:
                st.error("Please enter a numeric year")

    with col_right:
        if st.button("→"):
            st.session_state.year = min(max_year, st.session_state.year + 1)

  
    selected_year = st.session_state.year
    ##st.markdown(f"### Showing results for **{selected_year}**")
    df_year = df[df["year"] == selected_year]


    if "dept_births" in df.columns:
        df[["dept", "births"]] = df["dept_births"].str.split(",", expand=True)
        df = df.astype({"dept": "int", "births": "int"})
        df.drop(columns=["dept_births"], inplace=True)

    if selected_name:
        df = df[df["name"].str.lower() == selected_name.lower()]

    geojson = load_geojson()
    df2020 = df[df["year"] == selected_year]

    grp = (
        df2020
        .groupby(["dept", "name", "sex"], as_index=False)["births"]
        .sum()
    )
    grp["code"] = grp["dept"].apply(lambda d: f"{d:02d}")

    dept_hovers = []
    dept_codes = []

    for feat in geojson["features"]:
        code = feat["properties"]["code"]
        name_dep = feat["properties"].get("nom", code)

        dept_df = (
            grp[grp["code"] == code]
            .sort_values("births", ascending=False)
            .head(topN)
        )

        if dept_df.empty:
            hover_text = name_dep
        else:
            lines = [
                f"{row.name.capitalize()} ({'👧' if row.sex == 'F' else '👦'}): {int(row.births)}"
                for row in dept_df.itertuples()
            ]
            hover_text = name_dep + "<br>" + "<br>".join(lines)

        dept_codes.append(code)
        dept_hovers.append(hover_text)

    outline_df = pd.DataFrame({
        "code": dept_codes,
        "val": [1] * len(dept_codes),
        "hover": dept_hovers
    })

    chor = go.Choroplethmapbox(
        geojson=geojson,
        locations=outline_df.code,
        z=outline_df.val,
        featureidkey="properties.code",
        colorscale=[[0, "white"], [1, "white"]],
        showscale=False,
        marker_line_color="black",
        marker_line_width=0.6,
        hovertext=outline_df.hover,
        hoverinfo="text"
    )

    map_layers = []

    for feat in geojson["features"]:
        code = feat["properties"]["code"]
        poly = geom.shape(feat["geometry"])

        dept_df = (
            grp[grp["code"] == code]
            .sort_values("births", ascending=False)
            .head(topN)
        )

        if dept_df.empty:
            continue

        word_freqs = {
            row.name.capitalize(): int(row.births)
            for row in dept_df.itertuples()
        }

        area = poly.area
        scale = min(1.0, area / 0.5)
        img_width = max(80, int(180 * scale))
        img_height = max(60, int(120 * scale))

        padding = 0.6
        max_font = 45

        img_b64 = make_wordcloud_base64(
            word_freqs,
            img_width,
            img_height,
            padding_factor=padding,
            max_font=max_font
        )

        centroid = poly.centroid
        cx, cy = centroid.x, centroid.y
        dx = (poly.bounds[2] - poly.bounds[0]) * 0.2
        dy = (poly.bounds[3] - poly.bounds[1]) * 0.2

        map_layers.append({
            "sourcetype": "image",
            "source": "data:image/png;base64," + img_b64,
            "coordinates": [
                [cx - dx, cy + dy],
                [cx + dx, cy + dy],
                [cx + dx, cy - dy],
                [cx - dx, cy - dy]
            ],
            "opacity": 1.0
        })

    fig = go.Figure(chor)
    fig.update_layout(
        mapbox=dict(
            style="carto-positron",
            zoom=5.5,
            center={"lat": 46.5, "lon": 1.4},
            layers=map_layers
        ),
        margin=dict(t=0, l=0, r=0, b=0),
        height=750
    )

    st.plotly_chart(fig, use_container_width=True)
