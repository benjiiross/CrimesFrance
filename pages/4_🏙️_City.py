import streamlit as st
import pandas as pd
from tools.utility import set_page, load_main_dataset, load_comp_dataset
import plotly.graph_objects as go


def plot_city_crimes(df: pd.DataFrame, city_name: str) -> None:
    fig = go.Figure()

    for classe in df["classe"].unique():
        df_classe = df[df["classe"] == classe]
        fig.add_trace(
            go.Scatter(
                x=df_classe["annee"],
                y=df_classe["faits"],
                name=classe,
            )
        )

    fig.update_layout(
        title=f"Number of crimes recorded by police in {city_name}",
        xaxis_title="Year",
        yaxis_title="Number of crimes and offenses",
        height=600,
        width=800,
    )

    st.plotly_chart(fig)


def city() -> None:
    set_page("City")

    name = "donnee-data.gouv-2022-geographie2023-produit-le2023-07-17"
    df = load_main_dataset()
    st.dataframe(df.head(500))

    name = "info-complements-data.gouv-2022-geographie2023-produit-le2023-07-17"
    df_comp = load_comp_dataset()

    city = st.selectbox(
        "City", df_comp["city_dep"].unique(), placeholder="Select a city"
    )

    # Filter data for selected city. We need to remove the department code from the city name
    code_geo = df_comp[df_comp["city_dep"] == city]["CODGEO"].values[0]
    df_city = df[df["CODGEO_2023"] == code_geo]

    # for each classe draw a line of faits in fct of annee
    plot_city_crimes(df_city, str(city))

    st.markdown(
        "If you select a city located in the Bouches-du-Rhône department like Marseille or Cassis, you can see an abrupt increase in use of drugs in 2020."
        "This is because a new law was passed in 2020 that made it illegal to consume drugs in the street."
        "See more at [Le Monde](https://www.lemonde.fr/politique/article/2023/06/25/les-amendes-pour-consommation-de-drogue-pourront-etre-payables-immediatement-en-liquide-ou-carte-bancaire-a-annonce-emmanuel-macron_6179203_823448.html)"
    )


if __name__ == "__main__":
    city()
