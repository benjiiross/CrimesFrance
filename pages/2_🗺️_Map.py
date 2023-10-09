import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
from tools.utility import load_data, set_page, DEPARTMENT_DATA


@st.cache_data
def get_df_dep_plot(df: pd.DataFrame, year: int) -> pd.DataFrame:
    df_year = df[df["annee"] == year % 100]

    df_dep_plot = pd.DataFrame(
        columns=["Code_departement", "faits", "lat", "lon", "pop", "faits_per_hab"]
    )

    df_dep_plot["Code_departement"] = df_year["Code_departement"].unique()

    for dep in df_dep_plot["Code_departement"]:
        df_dep_plot.loc[df_dep_plot["Code_departement"] == dep, "faits"] = df_year.loc[
            df_year["Code_departement"] == dep
        ]["faits"].sum()

        df_dep_plot.loc[
            df_dep_plot["Code_departement"] == dep, "lat"
        ] = DEPARTMENT_DATA[dep]["lat"]
        df_dep_plot.loc[
            df_dep_plot["Code_departement"] == dep, "lon"
        ] = DEPARTMENT_DATA[dep]["lon"]

        df_dep_plot.loc[df_dep_plot["Code_departement"] == dep, "pop"] = df_year.loc[
            df_year["Code_departement"] == dep
        ]["POP"].iloc[0]

        df_dep_plot.loc[df_dep_plot["Code_departement"] == dep, "faits_per_hab"] = (
            df_dep_plot.loc[df_dep_plot["Code_departement"] == dep, "faits"]
            / df_dep_plot.loc[df_dep_plot["Code_departement"] == dep, "pop"]
        )

    return df_dep_plot


def france_map() -> None:
    set_page("Map")

    name = "donnee-dep-data.gouv-2022-geographie2023-produit-le2023-07-17"
    df_dep = load_data(f"./data/{name}.csv")

    year = st.slider(
        "Year",
        2016,
        2022,
        2016,
    )

    df_dep_plot = get_df_dep_plot(df_dep, year)
    activated = st.toggle("Toggle crim by habitants")

    # plot the map
    if activated:
        layer = (
            pdk.Layer(
                "ColumnLayer",
                data=df_dep_plot,
                get_position=["lon", "lat"],
                auto_highlight=True,
                get_elevation="faits_per_hab",
                elevation_scale=2000000,
                radius=10000,
                get_fill_color=[255, 140, 0],
                pickable=True,
            ),
        )
        r = pdk.Deck(
            map_style="",
            initial_view_state=pdk.ViewState(
                latitude=46.2276,
                longitude=2.2137,
                zoom=4,
                pitch=50,
            ),
            layers=[layer],
            tooltip={
                "html": "<b>Department:</b> {Code_departement} <br/> <b>Crimes by hab:</b> {faits_per_hab}",
                "style": {"color": "white"},
            },
        )
    else:
        layer = (
            pdk.Layer(
                "ColumnLayer",
                data=df_dep_plot,
                get_position=["lon", "lat"],
                auto_highlight=True,
                get_elevation="faits",
                radius=10000,
                get_fill_color=[255, 140, 0],
                pickable=True,
            ),
        )
        r = pdk.Deck(
            map_style="",
            initial_view_state=pdk.ViewState(
                latitude=46.2276,
                longitude=2.2137,
                zoom=4,
                pitch=50,
            ),
            layers=[layer],
            tooltip={
                "html": "<b>Department:</b> {Code_departement} <br/> <b>Crimes:</b> {faits}",
                "style": {"color": "white"},
            },
        )

    st.header(f"France map of crimes in {year}")
    st.pydeck_chart(r)


if __name__ == "__main__":
    france_map()
