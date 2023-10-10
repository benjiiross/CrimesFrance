import streamlit as st
from tools.utility import load_data, set_page
import time


def home() -> None:
    set_page("Home")

    # loads the dataset
    init_time: float = time.time()
    with st.spinner("Loading main dataset..."):
        name: str = "donnee-data.gouv-2022-geographie2023-produit-le2023-07-17"
        df = load_data(f"./data/{name}.csv")
        duration = time.time() - init_time

    init_time = time.time()
    with st.spinner("Loading departemental dataset..."):
        name: str = "donnee-dep-data.gouv-2022-geographie2023-produit-le2023-07-17"
        df_dep = load_data(f"./data/{name}.csv")

        # if we load the dataset for the 1st time
        if duration > 5:
            st.toast(
                f"Main dataset loaded! took {duration:.2f} seconds",
            )
            st.toast(
                f"Departemental dataset loaded! took {time.time() - init_time:.2f} seconds",
            )

    init_time: float = time.time()
    with st.spinner("Loading complementary datasets..."):
        name: str = (
            "info-complements-data.gouv-2022-geographie2023-produit-le2023-07-17"
        )
        df_comp = load_data(f"./data/{name}.xlsx")

        if duration > 2:
            st.toast(
                f"Complementary datasets loaded! took {time.time() - init_time:.2f} seconds",
            )
            st.snow()

    st.header(
        "Municipal and departmental statistics on crime recorded by the national police and gendarmerie in France"
    )

    st.write(
        "This dataset contains the number of crimes and offenses recorded by the national police and gendarmerie services in 2019, by municipality and department."
    )
    st.write(
        "The data is taken from the Ministry of the Interior's statistical service, the SSMI."
    )
    st.write(
        "The data is taken from the Ministry of the Interior's statistical service, the SSMI."
    )


if __name__ == "__main__":
    home()
