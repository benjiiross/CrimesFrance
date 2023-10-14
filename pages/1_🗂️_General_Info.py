import streamlit as st
import pandas as pd
import altair as alt
from tools.utility import (
    set_page,
    load_main_dataset,
    load_dep_dataset,
    get_crimes_per_year,
    center_metrics,
)


def dataset_info() -> None:
    set_page("General Info")

    df = load_main_dataset()
    df_dep = load_dep_dataset()
    df_year = get_crimes_per_year()

    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            label="Size of main dataset",
            value=f"{df.memory_usage().sum() / 1_000_000:.2f} MB",
        )

    with col2:
        st.metric(
            label="Size of department dataset",
            value=f"{df_dep.memory_usage().sum() / 1_000_000:.2f} MB",
        )
    st.divider()

    st.markdown(
        "<h1 style='text-align: center;'>Crimes per year</h1>",
        unsafe_allow_html=True,
    )

    nbr_rows = df_year.shape[0]
    cols = st.columns(nbr_rows)

    for i in range(nbr_rows):
        with cols[i]:
            year = df_year["annee"].iloc[i]
            population = format(df_year["population"].iloc[i], ",").replace(",", " ")

            if pd.isna(df_year["faits_previous_year"].iloc[i]):
                st.metric(
                    label=f"{year} : **{population}** hab",
                    value=format(df_year["faits"].iloc[i], ",").replace(",", " "),
                )
            else:
                st.metric(
                    label=f"{year} : **{population}** hab",
                    value=format(df_year["faits"].iloc[i], ",").replace(",", " "),
                    delta=f"{df_year['crime_relative_change'].iloc[i]}%",
                    delta_color="inverse",
                )

    st.info(
        r"""
        Please note that the crime relative change is calculated by comparing the number of crimes in a year with the number of crimes
        in the previous year:

        $$crime\_relative\_change_n = \frac{crimes_n - crimes_{n-1}}{crimes_{n-1}} * 100$$

        Where n is the year.

        Also, the dataset doesn't provide the population for 2021 and 2022, so we used the population from
        [INSEE](https://www.insee.fr/fr/statistiques/6686993?sommaire=6686521) (Institut National de la Statistique et des Etudes Economiques) for both years.
        """
    )
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        chart1 = (
            alt.Chart(df_year)
            .mark_line(size=7)
            .encode(
                x=alt.X("annee:O", axis=alt.Axis(labelAngle=0)),
                y=alt.Y(
                    "faits:Q",
                    scale=alt.Scale(domain=[2_000_000, df_year["faits"].max() * 1.1]),
                ),
                color=alt.value("red"),
            )
            .properties(title="Crimes per year", width=400, height=400)
        )
        st.altair_chart(chart1, use_container_width=True)

    with col2:
        chart2 = (
            alt.Chart(df_year)
            .mark_line(size=7)
            .encode(
                x=alt.X("annee:O", axis=alt.Axis(labelAngle=0)),
                y=alt.Y(
                    "population:Q",
                    scale=alt.Scale(domain=[66_000_000, 68_000_000]),
                ),
                color=alt.value("blue"),
            )
            .properties(title="Population per year", width=400, height=400)
        )
        st.altair_chart(chart2, use_container_width=True)

    st.warning(
        """
        Warning: The population for 2021 and 2022 is not yet available, so we used the estimated population from
        [INSEE](https://www.insee.fr/fr/statistiques/6686993?sommaire=6686521) for both years.
        """
    )

    st.info(
        """
        We can see a decrease in the number of crimes in 2020, which is due to the first lockdown in France.
        There is also a spike in crimes in 2021 and 2022 that compensates the decrease in 2020.
        Overall the most crimes from 2016 to 2022 are committed in 2022.

        For the 2023 year, we can expect to see an increase in crimes due to riots and protests against [Nahel's death](https://fr.wikipedia.org/wiki/Mort_de_Nahel_Merzouk).
        """
    )

    # chart3, crimes per 1000 inhabitants
    chart3 = (
        alt.Chart(df_year)
        .mark_line(size=7)
        .encode(
            x=alt.X("annee:O", axis=alt.Axis(labelAngle=0)),
            y=alt.Y(
                "faits_per_1000:Q",
                scale=alt.Scale(domain=[36, df_year["faits_per_1000"].max() * 1.1]),
            ),
            color=alt.value("green"),
        )
        .properties(title="Crimes per 1000 inhabitants", width=400, height=400)
    )
    st.altair_chart(chart3, use_container_width=True)

    st.info(
        """
        This graph shows the crimes per 1000 inhabitants. We can see that it follows the same trend as the crimes per year graph.

        Overall in France, we can deduce that there is around 42 crimes per 1000 inhabitants.
        """
    )

    center_metrics()


if __name__ == "__main__":
    dataset_info()
