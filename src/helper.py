"""Helper Functions."""

import pandas as pd
import streamlit as st


def include_matomo_stats() -> None:
    """Include Matomo access stats update JavaScript snippet."""
    import streamlit.components.v1 as components

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


def print_table_simple(df: pd.DataFrame) -> None:
    """Display simple table of few columns."""
    df["Dorf"] = df["Dorf"].round(0)
    st.dataframe(
        df,
        hide_index=True,
        use_container_width=True,
        column_order=["Titel", "Dorf"],  # , "Quelle", "Jahr"
        column_config={
            "Title": st.column_config.Column("Title", width="small"),
            "Dorf": st.column_config.ProgressColumn(
                format="%d", min_value=0, max_value=df["Dorf"].max(), width="large"
            ),
            # "Quelle": st.column_config.LinkColumn(
            #     "Quelle", display_text="Link"
            # ),
            # "Jahr": st.column_config.NumberColumn("Jahr", format="%d"),
        },
    )


def print_table_complete(df: pd.DataFrame) -> None:
    """Display complete data table."""
    df["Prozent"] = df["Prozent"].round(1)
    df["Dorf"] = df["Dorf"].round(1)
    st.dataframe(
        df.sort_values(["Gruppe", "Titel"]),
        hide_index=True,
        use_container_width=True,
        column_order=[
            "Gruppe",
            "Titel",
            "Personen",
            "Prozent",
            "Dorf",
            "Jahr",
            "Quelle",
            "Kommentar",
        ],  # , "Quelle", "Jahr"
        column_config={
            "Quelle": st.column_config.LinkColumn("Quelle", display_text="Link"),
            "Jahr": st.column_config.NumberColumn("Jahr", format="%d"),
            "Prozent": st.column_config.ProgressColumn(
                format="%.1f", min_value=0, max_value=100, width="large"
            ),
        },
    )
