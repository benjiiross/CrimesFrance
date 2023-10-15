import streamlit as st
import pandas as pd
from tools.utility import (
    set_page,
    load_comp_dataset,
    get_crimes_per_category_by_city,
    get_crimes_per_year_by_city,
)
import plotly.graph_objects as go
import plotly.express as px
import altair as alt


def city() -> None:
    set_page("City")

    df_comp = load_comp_dataset()

    col1, col2 = st.columns(2)

    with col1:
        city = st.selectbox(
            "City", df_comp["city_dep"].unique(), placeholder="Select a city"
        )
        df_city = get_crimes_per_category_by_city(str(city))

        st.markdown(
            f"""
            <h2 style="text-align: center;">
            {city}
            </h2>
            """,
            unsafe_allow_html=True,
        )

        col3, col4 = st.columns(2)
        with col3:
            st.markdown(
                f"""
                <h4 style="text-align: center;">
                Postal code: {df_comp[df_comp["city_dep"] == city]["CODGEO"].values[0]}
                </h2>
                """,
                unsafe_allow_html=True,
            )

        with col4:
            st.markdown(
                f"""
                <h4 style="text-align: center;">
                2020 population: {format(df_city[df_city["annee"] == 20]["POP"].values[0], ',').replace(',', '&nbsp;')}
                """,
                unsafe_allow_html=True,
            )

    with col2:
        df_city_pop = get_crimes_per_year_by_city(str(city))
        fig = px.line(
            df_city_pop, x="annee", y="population", title=f"Population of {city}"
        )
        # fig.update_layout(width=800, height=500)
        st.plotly_chart(fig, use_container_width=True)

    if df_city["faits"].sum() == 0:
        st.warning(f"There is no crime data for {city}.")
    else:
        col1, col2 = st.columns(2)

        with col1:
            fig = px.pie(
                df_city,
                values="faits",
                names="classe",
                title=f"Crimes in {city} by category",
            )
            fig.update_layout(width=800, height=500)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            chart = (
                alt.Chart(df_city)
                .mark_bar()
                .encode(
                    x=alt.X("annee:O", axis=alt.Axis(labelAngle=0), title="Year"),
                    y=alt.Y(
                        "faits:Q", stack="zero", sort="-x", title="Number of crimes"
                    ),
                    color="classe:N",
                )
                .properties(
                    title=f"Crimes in {city} by year",
                    width=800,
                    height=600,
                )
            )

            st.altair_chart(chart, use_container_width=True)

    if df_city["faits"].sum() != 0:
        fig = go.Figure()
        for classe in df_city["classe"].unique():
            df_classe = df_city[df_city["classe"] == classe]
            fig.add_trace(
                go.Scatter(
                    x=df_classe["annee"],
                    y=df_classe["faits"],
                    name=classe,
                )
            )
        fig.update_layout(
            title=f"Total crimes in {city} by year",
            xaxis_title="Year",
            yaxis_title="Number of crimes",
        )
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.warning(
        """
        The city population for 2021 and 2022 are not yet available, so their values is the same as 2020.
        """
    )

    st.info(
        """
        If you select a city located in the Bouches-du-Rhône department like Marseille or Cassis, you can see an abrupt
        increase in use of drugs in 2020. This is because a new law was passed in 2020 that made it illegal to consume drugs in the street.

        See more at [Le Monde](https://www.lemonde.fr/politique/article/2023/06/25/les-amendes-pour-consommation-de-drogue-pourront-etre-payables-immediatement-en-liquide-ou-carte-bancaire-a-annonce-emmanuel-macron_6179203_823448.html)
        """
    )

    st.info(
        """
        We can see that the vast majority of crimes in big cities are thefts and damage / destruction.
        In Paris, this is very pronounced with more than 50% of crimes being thefts.

        What is interesting is that still in Paris, the order of the crimes is the same as in the rest of France.
        So, we can conclude that Paris is a good indicator of what crimes are more common in France.
        """
    )


if __name__ == "__main__":
    city()
