import matplotlib.pyplot as plt  # para gráficas
import seaborn as sns  # para gráficas
import Acquisition.request as request # funciones para conectarse a la api
import time  # para simular datos en tiempo real(?)
import numpy as np  # análisis de datos
import pandas as pd  # manipulación de datos
import plotly.express as px  # gráficos interactivos
import streamlit as st  # 🎈 desarrollador de páginas web

st.set_page_config(
    page_title="FTX Dashboard",
    page_icon="📊",
    layout="wide",
)

# read csv from a URL
@st.experimental_memo
def get_data() -> pd.DataFrame:
    return request.actual_data()

df = get_data()

# dashboard title
st.title("Reporte de los mercados FTX")

# top-level filters
job_filter = st.selectbox("Elige el mercado que quieres ver", pd.unique(df["name"]))

# creating a single-element container
placeholder = st.empty()

# dataframe filter
df = df[df["name"] == job_filter]

# near real-time / live feed simulation
for seconds in range(200):

    df["age_new"] = df["age"] * np.random.choice(range(1, 5))
    df["balance_new"] = df["balance"] * np.random.choice(range(1, 5))

    # creating KPIs
    avg_age = np.mean(df["age_new"])

    count_married = int(
        df[(df["marital"] == "married")]["marital"].count()
        + np.random.choice(range(1, 30))
    )

    balance = np.mean(df["balance_new"])

    with placeholder.container():

        # create three columns
        kpi1, kpi2, kpi3 = st.columns(3)

        # fill in those three columns with respective metrics or KPIs
        kpi1.metric(
            label="Age ⏳",
            value=round(avg_age),
            delta=round(avg_age) - 10,
        )
        
        kpi2.metric(
            label="Married Count 💍",
            value=int(count_married),
            delta=-10 + count_married,
        )
        
        kpi3.metric(
            label="A/C Balance ＄",
            value=f"$ {round(balance,2)} ",
            delta=-round(balance / count_married) * 100,
        )

        # create two columns for charts
        fig_col1, fig_col2 = st.columns(2)
        with fig_col1:
            st.markdown("### First Chart")
            fig = px.density_heatmap(
                data_frame=df, y="age_new", x="marital"
            )
            st.write(fig)
            
        with fig_col2:
            st.markdown("### Second Chart")
            fig2 = px.histogram(data_frame=df, x="age_new")
            st.write(fig2)

        st.markdown("### Detailed Data View")
        st.dataframe(df)
        time.sleep(1)