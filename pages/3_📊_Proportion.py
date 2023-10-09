import streamlit as st
from tools.utility import load_data, set_page
import plotly.express as px


def proportion() -> None:
    set_page("Proportion")

    name = "donnee-data.gouv-2022-geographie2023-produit-le2023-07-17"
    df = load_data(f"./data/{name}.csv")

    name = "donnee-dep-data.gouv-2022-geographie2023-produit-le2023-07-17"
    df_dep = load_data(f"./data/{name}.csv")

    # make a slider to select a year
    year = st.slider("Year", 2016, 2022, 2016)

    # filter the data
    df_filtered = df_dep[df_dep["annee"] == year % 100]

    df_filtered = df_filtered.groupby("classe").sum()["faits"]

    fig = px.pie(
        df_filtered, values="faits", names=df_filtered.index, title=f"Crimes in {year}"
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(height=600, width=800)  # set the height and width of the chart
    st.plotly_chart(fig)

    city = st.selectbox("City", df["dep"].unique())

    st.write(f"Number of crimes in {city} in {year}:")


if __name__ == "__main__":
    proportion()
