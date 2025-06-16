import streamlit as st
import pandas as pd
import altair as alt
import random

COLOR = {"M": "#1f77b4", "F": "#e91e63"}

@st.cache_data
def load_data() -> pd.DataFrame:
    return pd.read_csv(st.session_state["NATIONAL_CSV"])


def peak_sentence(sub: pd.DataFrame) -> str:
    row = sub.loc[sub["births"].idxmax()]
    return (
        f"📌 Peak in {int(row.year)}: {int(row.births)} births "
        f"({'girls' if row.sex == 'F' else 'boys'})")


def top_names(df: pd.DataFrame, sex: str) -> pd.DataFrame:
    opp = "F" if sex == "M" else "M"
    return (
        df.groupby(["year", "name", "sex"])["births"].sum().unstack("sex", fill_value=0)
        .assign(sel=lambda d: d[sex], oth=lambda d: d[opp]).groupby("year")
        .apply(lambda g: g.nlargest(1, "sel")).reset_index(level=0, drop=True)
        .rename(columns={sex: "selected_sex_births", opp: "other_sex_births"})
        .assign(sex=sex).reset_index())


def top_unisex_names(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(["year", "name", "sex"], as_index=False)["births"]
        .sum().pivot(index=["year", "name"], columns="sex", values="births")
        .fillna(0).query("M>0 & F>0")
        .assign(delta=lambda d: (d.M - d.F).abs(), total=lambda d: d.M + d.F).reset_index()
        .sort_values(["year", "delta", "total"], ascending=[True, True, False]).groupby("year").first()
        .rename(columns={"M": "male_births", "F": "female_births"}).reset_index())


def main_charts(name_dict: dict[str, pd.DataFrame], names: list[str]) -> None:
    n = len(names)
    base_h, cols_per, rows = 280, 3, (n + 2) // 3

    for r in range(rows):
        cols = st.columns(cols_per)
        for c in range(cols_per):
            idx = r * cols_per + c
            if idx >= n: break
            name = names[idx]
            sub = name_dict.get(name)
            with cols[c]:
                if sub.empty:
                    st.warning(f"No data for {name}.")
                    continue
                if sub["year"].nunique() == 1:
                    base = alt.Chart(sub).mark_bar(opacity=0.3, size=20)
                else:
                    base = alt.Chart(sub).mark_area(opacity=0.3, interpolate="monotone")

                chart = (base.encode(
                        x=alt.X("year:O", axis=alt.Axis(labelAngle=0, title=None)),
                        y=alt.Y("births:Q", stack=None, title="Births"),
                        color=alt.Color("sex:N",scale=alt.Scale(domain=["M", "F"], range=[COLOR["M"], COLOR["F"]]),
                                        legend=alt.Legend(title="Gender", symbolType="circle")),
                        tooltip=["year:O", "births:Q", "sex:N"])
                         .properties(height=base_h, title=name).configure_axis(grid=False))
                st.altair_chart(chart, use_container_width=True)
                st.caption(peak_sentence(sub))


def top5_list(df_src: pd.DataFrame, *, unisex: bool = False) -> list[str]:
    if unisex:
        agg = df_src.groupby("name").agg(
            male_tot=("male_births", "sum"),
            female_tot=("female_births", "sum"))
        agg["delta"] = (agg["male_tot"] - agg["female_tot"]).abs()
        return agg.sort_values("delta").head(5).index.tolist()
    col = "selected_sex_births"
    return df_src.groupby("name")[col].sum().sort_values(ascending=False).head(5).index.tolist()


def fact_chart(df_fact: pd.DataFrame, title: str) -> alt.Chart:
    recs = []
    for _, row in df_fact.iterrows():
        yr, nm = row["year"], row["name"]
        if "selected_sex_births" in row:
            dom = row["sex"]
            recs.append({"year": yr, "name": nm, "births": row["selected_sex_births"], "sex": dom})
            recs.append({"year": yr, "name": nm, "births": row["other_sex_births"], "sex": "F" if dom == "M" else "M"})
        else:
            recs.append({"year": yr, "name": nm, "births": row["male_births"], "sex": "M"})
            recs.append({"year": yr, "name": nm, "births": row["female_births"], "sex": "F"})

    long = pd.DataFrame(recs)
    return (alt.Chart(long).mark_bar(opacity=0.8).encode(
            x=alt.X("year:O", axis=alt.Axis(labelAngle=0, title=None)),
            y="births:Q",
            color=alt.Color("sex:N", scale=alt.Scale(domain=["M", "F"], range=[COLOR["M"], COLOR["F"]]),
                            legend=alt.Legend(title="Gender")),
            tooltip=["year:O", "name:N", "births:Q", "sex:N"])
        .properties(height=320, title=title).configure_axis(grid=False))
    
def calc_top10_share(g):
    top10 = g.nlargest(10, "births")["births"].sum()
    total = g["births"].sum()
    return pd.Series({"share": top10 / total})


def display_visualization_3():
    st.subheader("🚻 Baby Name Gender Effect in France (1900-2020)")
    st.markdown("""
        <style>
        div[data-baseweb="select"] > div > div:first-child {
            flex-wrap: wrap !important;
            max-height: 150px;
            overflow-y: auto;
        }
        """,unsafe_allow_html=True,)

    df = load_data()
    if "name_dict" not in st.session_state:
        st.session_state["name_dict"] = {
            n: g.reset_index(drop=True) for n, g in df.groupby("name")
        }
    name_dict = st.session_state["name_dict"] 
    
    name_pool = sorted(df["name"].unique())
    if "selected_names" not in st.session_state:
        st.session_state["selected_names"] = random.sample(
            name_pool, min(4, len(name_pool)))

    selected = st.multiselect(
        label=" ",
        options=name_pool,
        key="selected_names",
        label_visibility="collapsed")

    if not selected:
        st.info("👆 Select at least one name to display its trajectory.")
        return

    main_charts(name_dict, selected)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🔍 Interesting facts")
    
    year_sex_total = df.groupby(["year", "sex"])["births"].sum().reset_index()
    year_sex_name = df.groupby(["year", "sex", "name"])["births"].sum().reset_index()

    top10_share = year_sex_name.groupby(["year", "sex"]).apply(calc_top10_share).reset_index()
    
    area_total = (alt.Chart(year_sex_total)
        .mark_area(interpolate="monotone", opacity=0.5).encode(
            x="year:O",
            y=alt.Y("births:Q", stack=None, title="Births"),
            color=alt.Color("sex:N", scale=alt.Scale(domain=["M","F"], range=[COLOR["M"], COLOR["F"]]),
                            legend=alt.Legend(title="Gender")))
        .properties(height=320, title="Total births by sex"))

    line_share = (alt.Chart(top10_share)
        .mark_line(interpolate="monotone").encode(
            x="year:O",
            y=alt.Y("share:Q", axis=alt.Axis(format="%"), title="Top-10 share"),
            color=alt.Color("sex:N", scale=alt.Scale(domain=["M","F"], range=[COLOR["M"], COLOR["F"]]),
                            legend=alt.Legend(title="Gender")))
        .properties(height=320, title="Name diversity (Top-10 share)"))

    col1, col2 = st.columns(2)
    with col1:
        st.altair_chart(area_total, use_container_width=True)
    with col2:
        st.altair_chart(line_share, use_container_width=True)
    
    male_top = top_names(df, "M")
    female_top = top_names(df, "F")
    unisex_top = top_unisex_names(df)

    facts = [(male_top, "Most-used boy names", top5_list(male_top)),
        (female_top, "Most-used girl names", top5_list(female_top)),
        (unisex_top, "Most-used unisex names", top5_list(unisex_top, unisex=True))]
    
    cols = st.columns(3)
    for col, (df_fact, title, topn) in zip(cols, facts):
        with col:
            st.altair_chart(fact_chart(df_fact, title), use_container_width=True)
            if topn:
                st.markdown(
                    "<b>🌟Top 5 popular names overall:</b><br>"
                    + "<br>".join(f"{i + 1}. {n}" for i, n in enumerate(topn)),
                    unsafe_allow_html=True)

