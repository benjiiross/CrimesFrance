import streamlit as st
from tools.utility import set_page, load_main_dataset, load_comp_dataset


def category_repartition() -> None:
    set_page("Category Repartition")

    name = "donnee-data.gouv-2022-geographie2023-produit-le2023-07-17"
    df = load_main_dataset()

    name = "info-complements-data.gouv-2022-geographie2023-produit-le2023-07-17"
    df_comp = load_comp_dataset()

    year = st.slider(
        "Year",
        2016,
        2022,
        2016,
    )

    category = st.selectbox(
        "Category",
        df["classe"].unique(),
        index=0,
    )
    activated = st.toggle("Toggle crim by habitants")

    df_year = df[df["annee"] == year % 100]
    df_category = df_year[df_year["classe"] == category]
    df_category["faits_per_hab"] = df_category["faits"] / df_category["POP"]

    # if activated, sort by faits_per_hab, else sort by faits
    if activated:
        df_category = df_category.sort_values(by="faits_per_hab", ascending=False)
        df_category = df_category.reset_index(drop=True)
    else:
        df_category = df_category.sort_values(by="faits", ascending=False)
        df_category = df_category.reset_index(drop=True)

    cities = df_category.head(10)
    cities = cities.rename(columns={"CODGEO_2023": "CODGEO"})
    cities = cities.merge(df_comp, on="CODGEO")

    cities = cities[["LIBGEO", "faits", "faits_per_hab", "POP", "DEP"]]
    cities = cities.rename(columns={"faits_per_hab": "faits / hab"})

    st.write(f"The most dangerous cities in {year} for the category '{category}' are:")

    st.dataframe(cities)


if __name__ == "__main__":
    category_repartition()
