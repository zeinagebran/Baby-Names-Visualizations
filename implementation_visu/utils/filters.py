def get_top_10_names(df):
    total_births = df.groupby(["name", "sex"])["births"].sum()
    top_10 = total_births.sort_values(ascending=False).head(10)
    # list of [name, sex, total_births]
    return top_10.reset_index().values.tolist()


def get_sudden_changes(df):
    name_scores = {}
    for (name, sex), sub_df in df.groupby(["name", "sex"]):
        sub_df = sub_df.sort_values("year")
        diffs = sub_df["births"].diff().abs().fillna(0)
        name_scores[(name, sex)] = diffs.max()
    sorted_names = sorted(name_scores.items(),
                          key=lambda x: x[1], reverse=True)
    return [(name, sex, max_change) for (name, sex), max_change in sorted_names[:10]]


def get_consistent_names(df, min_years=10):
    # Count number of years each name appears in
    name_year_counts = df.groupby(["name", "sex"])["year"].nunique()

    # Filter names that appear in at least `min_years` different years
    valid_names = name_year_counts[name_year_counts >= min_years].index

    # Filter the original DataFrame to only valid names
    filtered_df = df.set_index(["name", "sex"]).loc[valid_names].reset_index()

    # Calculate standard deviation of births for each name
    std_df = (
        filtered_df.groupby(["name", "sex"])["births"]
        .std()
        .reset_index(name="std_births")
    )

    # Select top 10 most stable names (lowest std)
    top_stable = std_df.sort_values("std_births").head(10)

    # Return list of tuples: [((name, sex), std_births)]
    return list(zip(top_stable[["name", "sex"]].apply(tuple, axis=1), top_stable["std_births"]))
