"""Main file."""

from pathlib import Path

import pandas as pd
import streamlit as st

from helper import include_matomo_stats

# must be first Streamlit command
st.set_page_config(
    page_title="DE-Dorf", page_icon=":derelict_house_building:", layout="wide"
)

if Path("/var/www/virtual/entorb/html").exists():
    include_matomo_stats()


st.title("Deutschland als Dorf")

# population for village, defaults to 2000
POP_DORF = st.session_state.get("sel_pop", 2000)

# text is copied from README.md
st.markdown("""
Um interessante Fakten zur deutschen Bevölkerung, wie beispielsweise "1.646.000 Millionäre", greifbarer zu machen, habe ich diese Zahlen auf ein Dorf mit 2000 Einwohnern umgerechnet. Das hilft mir, ein besseres Verständnis für die Welt außerhalb meiner eigenen sozialen Blase zu entwickeln. Das fiktive Dorf hätte dann 39 Millionäre, 41 geflüchtete Ukrainer und Syrer und 160 homo- oder bisexuelle Menschen.

### Mitmachen

Hast Du weitere interessante Zahlen oder Aktualisierungen? Dann schlag sie gerne direkt auf [GitHub](https://github.com/entorb/de-dorf/blob/main/data/data.tsv) vor. Alternativ kannst Du auch über [dieses Formular](https://entorb.net/contact.php?origin=de-dorf) Kontakt aufnehmen.
""")  # noqa: E501

df = pd.read_csv("data/population.tsv", sep="\t").astype(int).set_index("Jahr")
d_pop_per_year = df.to_dict()["Einwohner"]

df = pd.read_csv("data/data.tsv", sep="\t")

# calc people from percent
df.loc[df["Personen"].isna(), "Personen"] = (
    df["Prozent"] * 0.01 * df["Jahr"].map(d_pop_per_year.get)
).round(0)

# calc percent from people, no rounding here because of Dorf calc
df.loc[df["Prozent"].isna(), "Prozent"] = (
    100 * df["Personen"] / df["Jahr"].map(d_pop_per_year.get)
)

# convert to village population
df["Dorf"] = POP_DORF / 100 * df["Prozent"]

st.header("Kategorien")
for group in df["Gruppe"].unique().tolist():
    st.subheader(group)
    df2 = df[df["Gruppe"] == group].sort_values("Dorf", ascending=False)
    df2["Dorf"] = df["Dorf"].round(0)
    st.dataframe(
        df2,
        hide_index=True,
        column_config={
            "Title": st.column_config.Column("Title", width="small"),
            "Dorf": st.column_config.ProgressColumn(
                format="%d", min_value=0, max_value=df2["Dorf"].max(), width="large"
            ),
            "Quelle": st.column_config.LinkColumn(
                "Quelle", display_text="Link", width="small"
            ),
            "Jahr": st.column_config.NumberColumn("Jahr", format="%d", width="small"),
        },
        column_order=["Titel", "Dorf", "Quelle"],  # , "Jahr"
        use_container_width=True,
    )


st.header("Alle Daten")
df["Prozent"] = df["Prozent"].round(1)
df["Dorf"] = df["Dorf"].round(1)
st.dataframe(
    df.sort_values(["Gruppe", "Titel"]),
    hide_index=True,
    use_container_width=True,
    column_config={
        "Quelle": st.column_config.LinkColumn(
            "Quelle", display_text="Link", width="small"
        ),
        "Jahr": st.column_config.NumberColumn("Jahr", format="%d"),
        "Prozent": st.column_config.ProgressColumn(
            format="%.1f", min_value=0, max_value=100, width="large"
        ),
    },
)


st.header("Einstellungen")
sel_pop = st.slider("Anzahl Dorfbewohner", 100, 5000, 2000, 25, key="sel_pop")
