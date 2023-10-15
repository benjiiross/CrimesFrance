import streamlit as st
import base64
from tools.utility import set_page, show_presentation_file


def documentation() -> None:
    set_page("Documentation")

    st.info(
        """
        This official document presents the dataset used in this project. This PDF file written in french explains where the
        data comes from, how it was collected and how it is structured in the CSV files.
        """
    )

    show_presentation_file()


if __name__ == "__main__":
    documentation()
