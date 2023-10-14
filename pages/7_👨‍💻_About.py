import streamlit as st
from tools.utility import set_page


def about() -> None:
    set_page("About")
    st.snow()

    """
    Libraries used by page
    1. General Info: [Altair](https://altair-viz.github.io)
    1. Proportion: [Plotly](https://plotly.com/python)
    1. City: [Plotly](https://plotly.com/python)
    1. Map: [Pydeck](https://deckgl.readthedocs.io/en/latest)
    """

    # links to data.gouv.fr
    # me
    # when was it made


if __name__ == "__main__":
    about()
