import streamlit as st
from tools.utility import set_page, load_main_dataset, load_dep_dataset


def dataset_info() -> None:
    set_page("Dataset Info")

    df = load_main_dataset()

    name = "donnee-dep-data.gouv-2022-geographie2023-produit-le2023-07-17"
    df_dep = load_dep_dataset()

    st.dataframe(df.head(500))
    st.dataframe(df_dep)

    st.write("Number of values for each classe:")

    st.write(df["classe"].value_counts())


if __name__ == "__main__":
    dataset_info()
