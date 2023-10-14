import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
from tools.utility import load_dep_dataset, set_page, get_df_dep_lat_lon


def france_map() -> None:
    set_page("Map")

    df_dep = load_dep_dataset()

    col1, col2 = st.columns(2)

    with col1:
        year = st.slider(
            "Year",
            2016,
            2022,
            2016,
        )

    with col2:
        activated = st.toggle("Toggle crime per capita")

    df_dep_lat_lon = get_df_dep_lat_lon(df_dep, year)
    elevation = "faits_per_hab" if activated else "faits"
    elevation_scale = 2_000_000 if activated else 1

    layer = (
        pdk.Layer(
            "ColumnLayer",
            data=df_dep_lat_lon,
            get_position=["lon", "lat"],
            auto_highlight=True,
            get_elevation=elevation,
            elevation_scale=elevation_scale,
            radius=10_000,
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
            "html": "<b>Department:</b> {Code.département} <br/> <b>Crimes by hab:</b> {faits_per_hab}",
            "style": {"color": "white"},
        },
    )

    st.markdown(
        f"""
        <h1 style="text-align: center;">
        World map of crimes in {year} Metropolitan France and French overseas departments and territories
        </h1>
        """,
        unsafe_allow_html=True,
    )
    st.pydeck_chart(r)

    st.success(
        """
        The map is interactive, you can zoom in and out, and hover on a department to see its name and the number of crimes.

        You can also see the overseas departments, like Guadeloupe, Martinique, Guyane, Réunion and Mayotte.
        """
    )

    st.info(
        """
        We can see that around big cities there are a lot more crimes. This is normal because there are more people living there.

        With the toggle we can see that overall the criminality is the same in all departments at around 0.03/hab,
        but in the big cities there are more crimes by habitants.

        Overall Paris and the suburbs are the most dangerous places of France.
        """
    )


if __name__ == "__main__":
    france_map()
