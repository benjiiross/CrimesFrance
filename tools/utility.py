import streamlit as st
import pandas as pd
import requests
import io
import time
import base64


@st.cache_data
def load_main_dataset() -> pd.DataFrame:
    """
    Loads the main dataset of crimes in France from the data.gouv.fr website.
    To do so, it downloads the dataset from the website, and then reads it with pandas.

    Returns:
    --------
    pd.DataFrame
        A pandas DataFrame containing the loaded dataset.
    """

    main_dataset_path = (
        "https://www.data.gouv.fr/fr/datasets/r/3f51212c-f7d2-4aec-b899-06be6cdd1030"
    )
    response = requests.get(main_dataset_path)
    content = response.content
    df = pd.read_csv(
        io.BytesIO(content),
        sep=";",
        compression="gzip",
        low_memory=False,
    )
    return df


@st.cache_data
def load_dep_dataset() -> pd.DataFrame:
    """
    Loads the dataset of crimes in France by department from the data.gouv.fr website.
    To do so, it downloads the dataset from the website, and then reads it with pandas.

    Returns:
    --------
    pd.DataFrame
        A pandas DataFrame containing the loaded dataset.
    """

    dep_dataset_path = (
        "https://www.data.gouv.fr/fr/datasets/r/acc332f6-92be-42af-9721-f3609bea8cfc"
    )
    response = requests.get(dep_dataset_path)
    content = response.content
    df_dep = pd.read_csv(
        io.BytesIO(content),
        sep=";",
        compression="gzip",
        low_memory=False,
    )
    return df_dep


@st.cache_data
def load_comp_dataset() -> pd.DataFrame:
    """
    Loads the dataset of cities and geocodes from the data.gouv.fr website.
    To do so, it downloads the dataset from the website, and then reads it with pandas.

    Returns:
    --------
    pd.DataFrame
        A pandas DataFrame containing the loaded dataset.
    """

    comp_dataset_path = (
        "https://www.data.gouv.fr/fr/datasets/r/16ec626b-1a15-4512-a8ca-774921fc969e"
    )
    response = requests.get(comp_dataset_path)
    content = response.content
    df_comp = pd.read_excel(io.BytesIO(content), sheet_name="zonages supracommunaux")

    # add a column with the city name and department code to be able to filter
    df_comp["city_dep"] = df_comp["LIBGEO"] + " (" + df_comp["DEP"] + ")"
    return df_comp


def load_presentation_file():
    # path: str = "tools/documentation.pdf"

    # with open(path, "rb") as f:
    #     base64_pdf = base64.b64encode(f.read()).decode("utf-8")

    # # Embedding PDF in HTML
    # pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="1000" type="application/pdf"/>'

    # st.markdown(
    #     """
    # <embed src="https://raw.githubusercontent.com/benjiiross/CrimesFrance/main/tools/documentation.pdf" width="800" height="800">
    # """,
    #     unsafe_allow_html=True,
    # )
    # pdf_url = "https://raw.githubusercontent.com/benjiiross/CrimesFrance/main/tools/documentation.pdf"

    # pdf_display = f'<iframe src="{pdf_url}" width="700" height="700" type="application/pdf"></iframe>'

    # st.markdown(pdf_display, unsafe_allow_html=True)
    pdf_url = "https://raw.githubusercontent.com/benjiiross/CrimesFrance/main/tools/documentation.pdf"

    with st.spinner("Loading PDF..."):
        pdf_bytes = requests.get(pdf_url).content
        base64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="1000" type="application/pdf"/>'

    st.markdown(
        f"""
        <h1 style="text-align: center;">{pdf_display}</h1>
        """,
        unsafe_allow_html=True,
    )

    

def load_all_datasets() -> None:
    """
    Loads all the datasets used in the app.
    Times are showed in the status bar.
    """

    init_time = time.time()

    try:
        load_main_dataset()
        load_dep_dataset()
        load_comp_dataset()

        total_time = time.time() - init_time

        if total_time > 5:
            st.toast(f"Datasets loaded! took {total_time:.2f}s", icon="🚀")
            st.balloons()
        else:
            st.toast(f"Datasets reloaded! took {total_time:.2f}s", icon="🚀")

    except Exception as e:
        st.error("Error while loading the datasets. Please try again later.")
        st.exception(e)


@st.cache_data
def get_crimes_per_year() -> pd.DataFrame:
    """
    Returns the number of crimes per year.

    Returns:
    --------
    pd.DataFrame
        A pandas DataFrame containing the number of crimes per year, the population per year and the number of crimes per 1000 inhabitants.
    """
    df = load_dep_dataset()

    df_year = pd.DataFrame()

    df_year["annee"] = df["annee"].unique() + 2000

    df_year["faits"] = df.groupby("annee")["faits"].sum().values

    # get the population per year (we take the population of the first crime type we find)
    df_year["population"] = (
        df[df["classe"] == "Coups et blessures volontaires"]
        .groupby("annee")["POP"]
        .sum()
        .values
    )

    # since the dataset doesn't provide the population for 2021 and 2022, we use the INSEE estimation
    # https://www.insee.fr/fr/statistiques/6686993?sommaire=6686521
    INSEE_POPULATION = {
        2021: 67_635_124,
        2022: 67_842_591,
    }

    df_year.loc[df_year["annee"] == 2021, "population"] = INSEE_POPULATION[2021]
    df_year.loc[df_year["annee"] == 2022, "population"] = INSEE_POPULATION[2022]

    df_year["faits_previous_year"] = df_year["faits"].shift(1)
    df_year["crime_relative_change"] = (
        (df_year["faits"] - df_year["faits_previous_year"])
        / df_year["faits_previous_year"]
        * 100
    ).round(2)

    df_year["faits_per_1000"] = (df_year["faits"] / df_year["population"] * 1000).round(
        2
    )

    return df_year


@st.cache_data
def get_crimes_per_year_by_category(year: int) -> pd.DataFrame:
    """
    Returns the number of crimes per year by category.

    Parameters:
    -----------
    year: int
        The year to get the number of crimes from.

    Returns:
    --------
    pd.DataFrame
        A pandas DataFrame containing the number of crimes per year by category.
    """

    df_dep = load_dep_dataset()

    df_year: pd.DataFrame = df_dep[df_dep["annee"] == year % 100]
    df_year = df_year.groupby("classe").sum()["faits"].reset_index()
    df_year = df_year.sort_values(by="faits", ascending=False)

    return df_year


@st.cache_data
def get_crimes_per_category_by_city(city: str) -> pd.DataFrame:
    """
    Returns the number of crimes per year by category for a given city.

    Parameters:
    -----------
    city: str
        The city to get the number of crimes from.

    Returns:
    --------
    pd.DataFrame
        A pandas DataFrame containing the number of crimes per year by category for a given city.
    """
    df = load_main_dataset()
    df_comp = load_comp_dataset()

    code_geo = df_comp[df_comp["city_dep"] == city]["CODGEO"].values[0]
    df_city = df[df["CODGEO_2023"] == code_geo]

    return df_city


@st.cache_data
def get_crimes_per_year_by_city(city: str) -> pd.DataFrame:
    """
    Returns the number of crimes per year by city.

    Parameters:
    -----------
    city: str
        The city to get the number of crimes from.

    Returns:
    --------
    pd.DataFrame
        A pandas DataFrame containing the number of crimes per year by city.
    """
    df_city = get_crimes_per_category_by_city(city)

    df_year = pd.DataFrame()

    df_year["annee"] = df_city["annee"].unique() + 2000

    df_year["faits"] = df_city.groupby("annee")["faits"].sum().values

    # get the population per year (we take the population of the first crime type we find)
    df_year["population"] = (
        df_city[df_city["classe"] == "Coups et blessures volontaires"]
        .groupby("annee")["POP"]
        .sum()
        .values
    )

    # since the dataset doesn't provide the population for 2021 and 2022, we use the value from 2020
    df_year.loc[df_year["annee"] == 2021, "population"] = df_year.loc[
        df_year["annee"] == 2020, "population"
    ].values[0]
    df_year.loc[df_year["annee"] == 2022, "population"] = df_year.loc[
        df_year["annee"] == 2020, "population"
    ].values[0]

    return df_year

    return df_city


@st.cache_data
def get_most_dangerous_cities(
    year: int, category: str, activated: bool
) -> pd.DataFrame:
    df = load_main_dataset()
    df_comp = load_comp_dataset()

    df_year = df[df["annee"] == year % 100]
    df_category = df_year[df_year["classe"] == category]

    df_category.loc[:, "faits_per_hab"] = df_category["faits"] / df_category["POP"]

    # Sort based on the 'activated' flag
    column_to_sort = "faits_per_hab" if activated else "faits"
    df_category = df_category.sort_values(
        by=column_to_sort, ascending=False
    ).reset_index(drop=True)

    cities = df_category.head(10)
    cities = cities.rename(columns={"CODGEO_2023": "CODGEO"})

    # Merge with the complementary dataset
    cities = pd.merge(cities, df_comp, on="CODGEO")

    cities = cities[["LIBGEO", "faits", "faits_per_hab", "POP", "DEP"]]
    cities = cities.rename(columns={"faits_per_hab": "faits / hab"})

    return cities


@st.cache_data
def get_df_dep_lat_lon(df: pd.DataFrame, year: int) -> pd.DataFrame:
    df_year = df[df["annee"] == year % 100]

    unique_departments = df_year["Code.département"].unique()
    df_dep_plot = pd.DataFrame(
        {
            "Code.département": unique_departments,
            "faits": [
                df_year[df_year["Code.département"] == dep]["faits"].sum()
                for dep in unique_departments
            ],
            "lat": [DEPARTMENT_DATA[dep]["lat"] for dep in unique_departments],
            "lon": [DEPARTMENT_DATA[dep]["lon"] for dep in unique_departments],
            "pop": [
                df_year[df_year["Code.département"] == dep]["POP"].iloc[0]
                for dep in unique_departments
            ],
        }
    )

    df_dep_plot["faits_per_hab"] = df_dep_plot["faits"] / df_dep_plot["pop"]

    return df_dep_plot


def center_metrics() -> None:
    """
    Centers the metrics in the page.

    Returns:
    --------
    str
        A string containing the CSS code to center the metrics.
    """

    css = """
            [data-testid="metric-container"] {
                width: fit-content;
                margin: auto;
            }

            [data-testid="metric-container"] > div {
                width: fit-content;
                margin: auto;
            }

            [data-testid="metric-container"] label {
                width: fit-content;
                margin: auto;
            }
        """

    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def set_page(page: str) -> None:
    """
    Sets the page configuration.

    Parameters:
    -----------
    page: str
        The name of the page to set.
    """

    page_dict = {
        "Home": "🏠",
        "General Info": "🗂️",
        "Proportion": "📊",
        "City": "🏙️",
        "Cities & Categories": "🚨",
        "Map": "🗺️",
        "Documentation": "📖",
        "About": "👨‍💻",
    }

    st.set_page_config(
        page_title=f"{page} - Crime in France",
        page_icon=page_dict[page],
        layout="wide",
    )

    st.title(f"{page_dict[page]} {page}")
    st.divider()


DEPARTMENT_DATA = {
    "01": {"lat": 46.153425, "lon": 4.926114},
    "02": {"lat": 49.573157, "lon": 3.295646},
    "03": {"lat": 46.386281, "lon": 3.072794},
    "04": {"lat": 44.091493, "lon": 6.235997},
    "05": {"lat": 44.671234, "lon": 6.079957},
    "06": {"lat": 43.937999, "lon": 7.005844},
    "07": {"lat": 44.670126, "lon": 4.385752},
    "08": {"lat": 49.509086, "lon": 4.721674},
    "09": {"lat": 42.937241, "lon": 1.443596},
    "10": {"lat": 48.213008, "lon": 4.376782},
    "11": {"lat": 43.116573, "lon": 2.534962},
    "12": {"lat": 44.175496, "lon": 2.576660},
    "13": {"lat": 43.296174, "lon": 5.369952},
    "14": {"lat": 49.062617, "lon": -0.301173},
    "15": {"lat": 45.069722, "lon": 2.649001},
    "16": {"lat": 45.708008, "lon": 0.161069},
    "17": {"lat": 45.806978, "lon": -0.641816},
    "18": {"lat": 47.082680, "lon": 2.395383},
    "19": {"lat": 45.431350, "lon": 1.771625},
    "21": {"lat": 47.327529, "lon": 4.905620},
    "22": {"lat": 48.390394, "lon": -2.826694},
    "23": {"lat": 46.076141, "lon": 2.160872},
    "24": {"lat": 44.901986, "lon": 0.582307},
    "25": {"lat": 47.141788, "lon": 6.020063},
    "26": {"lat": 44.755128, "lon": 5.116361},
    "27": {"lat": 49.081667, "lon": 1.150000},
    "28": {"lat": 48.443001, "lon": 1.500000},
    "29": {"lat": 48.202047, "lon": -4.098617},
    "2A": {"lat": 41.918632, "lon": 8.738635},
    "2B": {"lat": 42.363660, "lon": 9.163171},
    "30": {"lat": 43.981125, "lon": 4.389374},
    "31": {"lat": 43.604652, "lon": 1.444209},
    "32": {"lat": 43.702633, "lon": 0.583333},
    "33": {"lat": 44.840440, "lon": -0.580500},
    "34": {"lat": 43.598763, "lon": 3.896140},
    "35": {"lat": 48.114719, "lon": -1.680024},
    "36": {"lat": 46.819332, "lon": 1.728136},
    "37": {"lat": 47.253741, "lon": 0.689508},
    "38": {"lat": 45.187560, "lon": 5.735781},
    "39": {"lat": 46.712128, "lon": 5.659919},
    "40": {"lat": 43.988427, "lon": -1.232432},
    "41": {"lat": 47.587471, "lon": 1.330511},
    "42": {"lat": 45.438384, "lon": 4.387146},
    "43": {"lat": 45.128444, "lon": 3.892138},
    "44": {"lat": 47.217250, "lon": -1.553360},
    "45": {"lat": 47.898071, "lon": 2.257423},
    "46": {"lat": 44.778301, "lon": 1.705572},
    "47": {"lat": 44.202148, "lon": 0.626953},
    "48": {"lat": 44.518333, "lon": 3.500000},
    "49": {"lat": 47.473434, "lon": -0.551188},
    "50": {"lat": 49.121060, "lon": -1.087197},
    "51": {"lat": 49.129484, "lon": 4.267068},
    "52": {"lat": 48.166667, "lon": 5.416667},
    "53": {"lat": 48.200001, "lon": -0.500000},
    "54": {"lat": 48.666668, "lon": 6.166667},
    "55": {"lat": 48.983334, "lon": 5.366667},
    "56": {"lat": 47.750000, "lon": -3.000000},
    "57": {"lat": 49.000000, "lon": 6.833333},
    "58": {"lat": 47.000000, "lon": 3.500000},
    "59": {"lat": 50.500000, "lon": 3.000000},
    "60": {"lat": 49.416668, "lon": 2.500000},
    "61": {"lat": 48.583332, "lon": 0.500000},
    "62": {"lat": 50.500000, "lon": 2.500000},
    "63": {"lat": 45.750000, "lon": 3.000000},
    "64": {"lat": 43.250000, "lon": -0.750000},
    "65": {"lat": 43.000000, "lon": 0.000000},
    "66": {"lat": 42.500000, "lon": 2.750000},
    "67": {"lat": 48.583332, "lon": 7.500000},
    "68": {"lat": 47.916668, "lon": 7.166667},
    "69": {"lat": 45.750000, "lon": 4.833333},
    "70": {"lat": 47.666668, "lon": 6.166667},
    "71": {"lat": 46.833332, "lon": 4.500000},
    "72": {"lat": 48.000000, "lon": 0.166667},
    "73": {"lat": 45.500000, "lon": 6.000000},
    "74": {"lat": 46.000000, "lon": 6.500000},
    "75": {"lat": 48.856614, "lon": 2.3522219},
    "76": {"lat": 49.500000, "lon": 1.000000},
    "77": {"lat": 48.833332, "lon": 2.666667},
    "78": {"lat": 48.750000, "lon": 1.916667},
    "79": {"lat": 46.333332, "lon": -0.666667},
    "80": {"lat": 49.900002, "lon": 2.333333},
    "81": {"lat": 43.933334, "lon": 2.166667},
    "82": {"lat": 44.000000, "lon": 1.500000},
    "83": {"lat": 43.416668, "lon": 6.000000},
    "84": {"lat": 44.166668, "lon": 5.166667},
    "85": {"lat": 46.666668, "lon": -1.166667},
    "86": {"lat": 46.583332, "lon": 0.333333},
    "87": {"lat": 45.833332, "lon": 1.250000},
    "88": {"lat": 48.166668, "lon": 6.500000},
    "89": {"lat": 47.800003, "lon": 3.566667},
    "90": {"lat": 47.633331, "lon": 6.866667},
    "91": {"lat": 48.583332, "lon": 2.333333},
    "92": {"lat": 48.900002, "lon": 2.233333},
    "93": {"lat": 48.916668, "lon": 2.416667},
    "94": {"lat": 48.800003, "lon": 2.483333},
    "95": {"lat": 49.000000, "lon": 2.166667},
    "971": {"lat": 16.250000, "lon": -61.583332},
    "972": {"lat": 14.666667, "lon": -61.000000},
    "973": {"lat": 4.000000, "lon": -53.000000},
    "974": {"lat": -21.166668, "lon": 55.500000},
    "976": {"lat": -12.833332, "lon": 45.166668},
}
