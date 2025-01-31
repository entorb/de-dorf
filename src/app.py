"""Main file."""

from pathlib import Path

import pandas as pd
import streamlit as st

from helper import (
    include_matomo_stats,
    print_table_complete,
    print_table_simple,
    read_data,
)

# must be first Streamlit command
st.set_page_config(
    page_title="Deutschland als Dorf",
    page_icon=":derelict_house_building:",
    layout="wide",
)

if Path("/var/www/virtual/entorb/html").exists():
    include_matomo_stats()


st.title("Deutschland als Dorf")


# text is copied from README.md
st.markdown("""
Um interessante Fakten zur deutschen Bevölkerung, wie beispielsweise "1.6 Mill. Millionäre", greifbarer zu machen, habe ich diese Zahlen auf ein Dorf mit 2000 Einwohnern umgerechnet. Das hilft mir, ein besseres Verständnis für die Welt außerhalb meiner eigenen sozialen Blase zu entwickeln. Das fiktive Dorf hätte dann 39 Millionäre, 41 geflüchtete Ukrainer und Syrer und 160 homo- oder bisexuelle Menschen.

Viel Spaß damit wünscht Torben

### Mitmachen

Hast Du weitere interessante Zahlen gefunden oder möchtest Aktualisierungen beisteuern? Dann schlag sie gerne direkt auf [GitHub](https://github.com/entorb/de-dorf/blob/main/data/data.tsv) vor. Alternativ kannst Du auch über [dieses Formular](https://entorb.net/contact.php?origin=de-dorf) Kontakt aufnehmen und Verbesserungsvorschläge einreichen.
""")  # noqa: E501


# population for village, defaults to 2000
pop = st.session_state.get("sel_pop", 2000)
df = read_data(pop)
categories = df["Kategorie"].unique().tolist()
# sort after extracting the groups in custom order
df = df.sort_values(["Kategorie", "Titel"])

st.header("Alle Daten")
print_table_complete(df)


st.header("Kategorien")
cols = st.columns((1, 5))
sel_compact_layout = cols[0].toggle("kompaktes Layout", value=False)

num_columns = 2 if sel_compact_layout else 1
cols = st.columns(num_columns)
i = 0
for cat in categories:
    cols[i].subheader(cat)
    df2 = df[df["Kategorie"] == cat]
    print_table_simple(df2, cols[i], show_source=False)
    i = (i + 1) % num_columns
    if i == 0 and sel_compact_layout is True:
        cols = st.columns(num_columns)


st.header("Eigene Tabelle")

num_columns = 6 if sel_compact_layout else 3
cols = st.columns(num_columns)

selects = []
i = 0
for cat in categories:
    selects.append(
        cols[i].multiselect(
            label=cat,
            options=df.query("Kategorie == @cat")["Titel"].sort_values(),
            key=f"sel_custom_table_{cat}",
        )
    )
    i = (i + 1) % num_columns

dfs = [df.query("Titel in @sel") for sel in selects if sel]

if len(dfs) > 0:
    df2 = pd.concat(dfs)
    num_columns = 2 if sel_compact_layout else 1
    cols = st.columns(num_columns)

    # print_table_complete(df2.sort_values(["Prozent", "Titel"], ascending=[False, True]))  # noqa: E501
    print_table_simple(df2, col=cols[0], show_source=False)


st.header("Einstellungen")
sel_pop = st.slider("Anzahl Dorfbewohner", 100, 5000, 2000, 25, key="sel_pop")

# read and drop title line (# )
cont = Path("Weitere_Zahlen.md").read_text().split("\n", 1)[1]

st.markdown(cont)

# toggle_dark = st.toggle("Dark Layout", value=True)
# if st.get_option("theme.base") == "light" and toggle_dark:
#     st._config.set_option("theme.base", "dark")  # type: ignore
#     st.rerun()
# elif st.get_option("theme.base") == "dark" and not toggle_dark:
#     st._config.set_option("theme.base", "light")  # type: ignore
#     st.rerun()
