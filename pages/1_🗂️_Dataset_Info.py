import streamlit as st
from tools.utility import load_data, set_page

def dataset_info() -> None:
    set_page("Dataset Info")

    name = "donnee-data.gouv-2022-geographie2023-produit-le2023-07-17"
    df = load_data(f"./data/{name}.csv")

    name = "donnee-dep-data.gouv-2022-geographie2023-produit-le2023-07-17"
    df_dep = load_data(f"./data/{name}.csv")

    st.dataframe(df.head(500))
    st.dataframe(df_dep)

    st.write("Number of values for each classe:")

    st.write(df["classe"].value_counts())


if __name__ == "__main__":
    dataset_info()
