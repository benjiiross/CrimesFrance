import streamlit as st
from tools.utility import set_page


def about() -> None:
    set_page("About")
    st.snow()

    st.markdown("""## Who made this?""")
    st.success(
        "This app was made by [Benjamin](https://www.linkedin.com/in/benjamin-berhault-2b1b0b1a4/) in October 2023."
    )

    st.markdown("""## Why was it made?""")
    st.success(
        "This app was made for the Data Visualization course of the Master 1 Data Science at EFREI Paris. #datavz2023efrei"
    )

    st.markdown("""## Where does the data come from?""")
    st.success(
        "The data comes from the [French government](https://www.data.gouv.fr/fr/datasets/bases-statistiques-communale-et-departementale-de-la-delinquance-enregistree-par-la-police-et-la-gendarmerie-nationales)."
    )

    st.markdown("""## How was it made?""")
    st.success(
        "This app was made with [Streamlit](https://streamlit.io) and [Python](https://www.python.org)."
    )

    st.markdown("""## What libraries were used?""")
    st.success(
        """
                🗂️ General Info: [Altair](https://altair-viz.github.io)

                📊 Proportion: [Plotly](https://plotly.com/python)

                🏙️ City: [Plotly](https://plotly.com/python) and [Altair](https://altair-viz.github.io)

                🗺️ Map: [Pydeck](https://deckgl.readthedocs.io/en/latest)
                """
    )


if __name__ == "__main__":
    about()
