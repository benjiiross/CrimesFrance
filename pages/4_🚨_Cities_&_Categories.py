import streamlit as st
from tools.utility import set_page, load_main_dataset, get_most_dangerous_cities


def category_repartition() -> None:
    set_page("Cities & Categories")

    df = load_main_dataset()

    col1, col2 = st.columns(2)
    with col1:
        col3, col4 = st.columns(2)
        with col3:
            year = st.slider(
                "Year",
                2016,
                2022,
                2016,
            )
        with col4:
            activated = st.toggle("Toggle crime per capita")

        category = st.selectbox(
            "Category",
            df["classe"].unique(),
            index=0,
        )

        cities = get_most_dangerous_cities(year, str(category), activated)

    with col2:
        st.write(
            f"The most dangerous cities in {year} for the category '{category}' are:"
        )
        st.dataframe(cities)

    st.info(
        """
        We get some interesting results with the toggle:

        We can see that the most dangerous cities concerning weapons are mainly overseas.

        We can also see that with the toggle, Le Mont-Saint-Michel is in 2022 the most dangerous city concerning steal without violence.
        This is because there are very few people that live in the city. Obviously with 36 crimes, the city is not dangerous. So, we need
        to take into account what is the average number of crimes for the selected category.
        Nevertheless, we can see that the toggle is useful to compare cities with different populations.

        Overall the most dangerous cities are big cities, like Paris, Marseille, Lyon, Bordeaux, etc.
        """
    )


if __name__ == "__main__":
    category_repartition()
