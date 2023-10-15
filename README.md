# CrimesFrance

## Description

This project is a web application that allows you to visualize the crimes in France. It is based on the data of the French Ministry of the Interior.

This website uses Streamlit: it is deployed on [crimesfrance.streamlit.app](https://crimesfrance.streamlit.app/)

For more information: [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/bases-statistiques-communale-et-departementale-de-la-delinquance-enregistree-par-la-police-et-la-gendarmerie-nationales/)

## Installation

### Prerequisites

You need python3 installed. You can enter the following command from a terminal to check if it is installed:

```bash
python --version
```

### Clone the repository

```bash
git clone https://github.com/benjiiross/CrimesFrance.git
cd CrimesFrance
```

### Install the dependencies

To do so, you can create a virtual environment using conda (faster than pip)

```bash
conda create -n streamlit_Benjamin_ROSSIGNOL -y
```

Then activate it:

```bash
conda activate streamlit_Benjamin_ROSSIGNOL
conda install pip -y
```

Finally, install the dependencies:

```bash
pip install -r requirements.txt
```

Then you can run the application:

```bash
streamlit run 0_🏠_Home.py
```

And you can access the application on your browser at the following address: [localhost:8501](http://localhost:8501/)

After using the app you can delete the virtual environment:

```bash
conda deactivate
conda remove -n streamlit_Benjamin_ROSSIGNOL --all -y
```
