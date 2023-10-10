import streamlit as st
import pandas as pd
from tools.utility import load_data, set_page
import plotly.graph_objects as go


def plot_city_crimes(df: pd.DataFrame, city_name) -> None:
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
    df = load_data(f"./data/{name}.csv")

    name = "info-complements-data.gouv-2022-geographie2023-produit-le2023-07-17"
    df_comp = load_data(f"./data/{name}.xlsx")

    city = st.selectbox("City", df_comp["LIBGEO"].unique(), placeholder="Select a city")

    # Filter data for selected city
    code_geo = df_comp[df_comp["LIBGEO"] == city]["CODGEO"].values[0]
    df_city = df[df["CODGEO_2023"] == code_geo]

    # for each classe draw a line of faits in fct of annee
    plot_city_crimes(df_city, city)

    st.write(
        "If you select a city located in the Bouches-du-Rhône department like Marseille or Cassis, you can see an abrupt increase in use of drugs in 2020. This is because a new law was passed in 2020 that made it illegal to consume drugs in the street."
    )

    st.markdown(
        "See more at [Le Monde](https://www.lemonde.fr/politique/article/2023/06/25/les-amendes-pour-consommation-de-drogue-pourront-etre-payables-immediatement-en-liquide-ou-carte-bancaire-a-annonce-emmanuel-macron_6179203_823448.html)"
    )


if __name__ == "__main__":
    city()
