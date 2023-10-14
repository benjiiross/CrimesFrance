import streamlit as st
from tools.utility import set_page, get_crimes_per_year_by_category
import plotly.express as px


def proportion() -> None:
    set_page("Proportion")

    year = st.slider("Year", 2016, 2022, 2016)
    df_year = get_crimes_per_year_by_category(year)

    fig = px.pie(
        df_year,
        values="faits",
        names=df_year["classe"],
        title=f"Crimes in {year} in France",
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(height=600, width=800)
    st.plotly_chart(fig, use_container_width=True)

    st.info(
        """
        We can see that the most common crimes are **Non-violent theft from persons** and **Intentional damage and destruction**.
        They mainly apprear in big cities like Paris, Marseille, Lyon, Bordeaux, etc.

        We can also see that the categories are not exclusive, so a crime can be in multiple categories.
        Also, the categories are quite restrictive: **Cybercrime**, **Missing** or **Fraud** are not included in the dataset.
        """
    )

    st.error(
        """
        **Important note:** from the documentation, we can read that:
        > *only 12% of victims of sexual violence lodge a complaint, compared with 74% of victims of burglary.*

        It means that the data is not representative of the reality: the number of crimes is much higher than the number of crimes recorded by the police.

        To put that into perspective, it would put sexual violence at the 3rd place of the most common crimes.
        This questions the reliability of the dataset and the conclusions we can draw from it.
        """
    )

    st.info(
        """
        There are also other factors that can influence the data:

        > *Data is limited to municipalities where more than 5 incidents have been recorded during 3 successive years*

        It means that some cities are not included in the dataset because they are too small, or too few crimes are recorded.
        So, some crimes are missing from the dataset.

        > *The recording delay, which can create a time lag between when the offences occur and the time at which they are recorded*

        It means that some crimes are recorded in the wrong year, which can slightly alter the results.
        """
    )


if __name__ == "__main__":
    proportion()
