def get_top_10_names(df):
    return (
        df.groupby(["name", "sex"])["births"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .index.tolist()
    )


def get_sudden_changes(df):
    name_scores = {}
    for (name, sex), sub_df in df.groupby(["name", "sex"]):
        sub_df = sub_df.sort_values("year")
        diffs = sub_df["births"].diff().abs().fillna(0)
        name_scores[(name, sex)] = diffs.max()
    sorted_names = sorted(name_scores.items(),
                          key=lambda x: x[1], reverse=True)
    return [pair for pair, _ in sorted_names[:10]]


def get_consistent_names(df):
    return (
        df.groupby(["name", "sex"])["births"]
        .std()
        .sort_values()
        .head(10)
        .index.tolist()
    )
