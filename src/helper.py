"""Helper Functions."""

import pandas as pd
import streamlit as st
from streamlit.delta_generator import DeltaGenerator


@st.cache_data(ttl="1d")
def read_data(pop: int) -> pd.DataFrame:
    """Read and prepare the data (cached)."""
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

    # convert to village population (float without rounding here to prevent 2x rounding)
    df["Dorf"] = pop / 100 * df["Prozent"]
    return df


def print_table_simple(
    df: pd.DataFrame, col: DeltaGenerator, *, show_source: bool
) -> None:
    """Display simple table of few columns."""
    df = df.sort_values(["Dorf", "Titel"], ascending=[False, True])
    df["Dorf"] = df["Dorf"].round(1)
    col_order = ["Titel", "Dorf"]
    if show_source:
        col_order.append("Quelle")
    col.dataframe(
        df,
        hide_index=True,
        width="stretch",
        column_order=col_order,
        column_config={
            "Title": st.column_config.Column("Title", width="small"),
            "Dorf": st.column_config.ProgressColumn(
                label="Personen im Dorf",
                format="%.1f",
                min_value=0,
                max_value=df["Dorf"].max(),
                # width="large", # breaks mobile layout
            ),
            "Quelle": st.column_config.LinkColumn("Quelle", display_text="Link"),
        },
    )


def print_table_complete(df: pd.DataFrame) -> None:
    """Display complete data table."""
    df["Prozent"] = df["Prozent"].round(2)
    df["Dorf"] = df["Dorf"].round(1)
    st.dataframe(
        df,
        hide_index=True,
        width="stretch",
        column_order=[
            "Kategorie",
            "Titel",
            "Personen",
            "Prozent",
            "Dorf",
            "Quelle",
            "Jahr",
            "Kommentar",
        ],
        column_config={
            "Quelle": st.column_config.LinkColumn("Quelle", display_text="Link"),
            "Jahr": st.column_config.NumberColumn("Jahr", format="%d"),
            "Dorf": st.column_config.NumberColumn("Im Dorf", format="%.1f"),
            "Prozent": st.column_config.ProgressColumn(
                format="%.2f",
                min_value=0,
                max_value=100,
                # width="large" # breaks mobile layout
            ),
        },
    )


@st.cache_data(ttl="1d")
def read_flaechennutzung() -> pd.DataFrame:
    """Read and prepare the data of Flächennutzung (cached)."""
    df = pd.read_csv("data/flaechennutzung.csv", sep=";")
    df = df.drop(columns=["Code", "Jahr", "Quelle"])

    last = df.tail(1)
    qkm_total = last["qkm"].to_list()[0]
    df = df.drop(last.index)
    df["Prozent"] = (100 * df["qkm"] / qkm_total).round(2)
    # df = df.sort_values(
    #     ["Kategorie 1", "Kategorie 2", "Prozent"], ascending=[True, True, False]
    # )
    # df = df.sort_values("Prozent", ascending=False)

    return df


@st.cache_data(ttl="1d")
def read_countries(pop: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Read and prepare the data of country population (cached).

    returns df for countries and df for continents
    """
    df1 = pd.read_csv("data/countries.tsv", sep="\t")
    df1 = df1.drop(columns=["Jahr"])
    df1 = df1.sort_values("Einwohner", ascending=False)

    # Kontinente
    df2 = (
        df1.groupby("Kontinent")
        .agg(Einwohner=("Einwohner", "sum"))
        .sort_values("Einwohner", ascending=False)
    ).reset_index()

    total = df2["Einwohner"].sum()
    df1["Dorf"] = (df1["Einwohner"] / total * pop).round(0)
    df2["Dorf"] = (df2["Einwohner"] / total * pop).round(0)

    return df1, df2


def init_sentry() -> None:
    """Initialize Sentry exception tracking/alerting."""
    import sentry_sdk  # noqa: PLC0415

    sentry_sdk.init(
        dsn=st.secrets["sentry_dsn"],
        environment="entorb.net",
        send_default_pii=True,
        traces_sample_rate=0.0,
    )


def init_matomo() -> None:
    """Initialize Matomo access stats, via JavaScript snippet."""
    import streamlit.components.v1 as components  # noqa: PLC0415

    components.html(
        """
<script>
var _paq = window._paq = window._paq || [];
_paq.push(['trackPageView']);
_paq.push(['enableLinkTracking']);
(function() {
    var u="https://entorb.net/stats/matomo/";
    _paq.push(['setTrackerUrl', u+'matomo.php']);
    _paq.push(['setSiteId', '7']);
    var d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')[0];
    g.async=true; g.src=u+'matomo.js'; s.parentNode.insertBefore(g,s);
})();
</script>
    """,
        height=0,
    )
