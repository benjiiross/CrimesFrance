import streamlit as st
import base64
from tools.utility import set_page, load_presentation_file


def documentation() -> None:
    set_page("Documentation")

    st.info(
        """
        This official document presents the dataset used in this project. This PDF file written in french explains where the
        data comes from, how it was collected and how it is structured in the CSV files.
        """
    )

    # path: str = "tools/documentation.pdf"

    # with open(path, "rb") as f:
    #     base64_pdf = base64.b64encode(f.read()).decode("utf-8")

    # # Embedding PDF in HTML
    # pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="1000" type="application/pdf"/>'

    # st.markdown(pdf_display, unsafe_allow_html=True)

    load_presentation_file()


if __name__ == "__main__":
    documentation()
