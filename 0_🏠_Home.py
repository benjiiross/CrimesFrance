import streamlit as st
from tools.utility import (
    set_page,
    load_all_datasets,
)


def home() -> None:
    set_page("Home")
    load_all_datasets()

    """
    # Statistical bases of the delinquency recorded by the police and the national french gendarmerie
    :gray[by Benjamin ROSSIGNOL, 2023]

    The statistical bases of the delinquency recorded by the french police and gendarmerie come from the
    *Service statistique ministériel de la sécurité intérieure*, the SSMSI (or Ministerial Statistical Service for Internal Security).

    These offences may have been recorded following a complaint lodged by a victim, a report, testimony, flagrante delicto,
    denunciation, etc., but also on the initiative of the security forces.

    The dataset is composed of 4 files:
    - **Municipal** statistical database on crime recorded by the national police and gendarmerie
    - **Departmental** statistics on crime recorded by the national police and gendarmerie
    - **Complementary** file to the communal statistical base of delinquency which contains **city names**, **city types** and related **department numbers**
    - **Presentation** of municipal and departmental statistics on crime recorded by the national police and gendarmerie (**Official document**)

    This website is a data visualization of all files. It is made with Streamlit and Python using various libraries.

    Here is the link of the dataset for reference: [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/bases-statistiques-communale-et-departementale-de-la-delinquance-enregistree-par-la-police-et-la-gendarmerie-nationales/)
    """

    st.success(
        "If you have any reclamations or questions, please contact me by [email](mailto:benjamin.rossignol.11@gmail.com) or on [GitHub](https://github.com/benjiiross). If you want to run the project you can visit the [GitHub repository](https://github.com/benjiiross/CrimesFrance)"
    )


if __name__ == "__main__":
    home()
