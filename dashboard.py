import matplotlib.pyplot as plt  # para gráficas
import seaborn as sns  # para gráficas
import Acquisition.request as request # funciones para conectarse a la api
import time  # para simular datos en tiempo real(?)
import numpy as np  # análisis de datos
import pandas as pd  # manipulación de datos
import plotly.express as px  # gráficos interactivos
import streamlit as st  # 🎈 desarrollador de páginas web

# Se configura la página
st.set_page_config(
    page_title="FTX Dashboard",
    page_icon="📊",
    layout="wide",
)

# Lista de mercados que nos interesan
markets_to_use = ['BTC/USD', 'ETH/USD', 'USDT/USD', 'BNB/USD', 'XRP/USD', 'SOL/USD', 'DOGE/USD', 'DOT/USD', 'DAI/USD', 'MATIC/USD']

# Título del dashboard
st.title("Reporte de los mercados FTX")
st.write('***')

# Se crea el contenedor de los datos que se actializan
placeholder = st.empty()

# Actualización de los datos en "tiempo real"
for seconds in range(200):
    # Lectura de los datos con los mercados que nos interesan
    df = request.actual_data()
    df = df[df.name.isin(markets_to_use)]
    df.reset_index(drop=True, inplace=True)

    with placeholder.container():

        # se crea la primera fila de 5 columnas para la mitad del valor de los mercados
        m1, m2, m3, m4, m5 = st.columns(5)
        var_m = [m1, m2, m3, m4, m5]
        k = 0
        # se configura cada columna con los valores del dataframe teniendo como referencia la
        # lista market_to_use, si se cambia la lista estos valores cambian automáticamente
        for j in var_m:
            # se obtiene el índice de cada mercado que contiene la lista market_to_use
            i = df.index[(df['name'] == markets_to_use[k])].tolist()[0]
            # se itera con cada variable m para darle el valor del dataframe con el índice anterior
            j.metric(
                label = df['name'][i],
                value = df['bid'][i],
                delta = round(df['change24h'][i]*100,2),
            )
            k += 1
        # igual que la columna anterior, en esta se llenan con losvalores de los 5 últimos mercados
        m1, m2, m3, m4, m5 = st.columns(5)
        var_m = [m1, m2, m3, m4, m5]
        for j in var_m:
            i = df.index[(df['name'] == markets_to_use[k])].tolist()[0]
            j.metric(
                label = df['name'][i],
                value = df['bid'][i],
                delta = round(df['change24h'][i]*100,2),
            )
            k += 1
        #  )
        # # create two columns for charts
        # fig_col1, fig_col2 = st.columns(2)
        # with fig_col1:
        #     st.markdown("### First Chart")
        #     fig = px.density_heatmap(
        #         data_frame=df, y="age_new", x="marital"
        #     )
        #     st.write(fig)
            
        # with fig_col2:
        #     st.markdown("### Second Chart")
        #     fig2 = px.histogram(data_frame=df, x="age_new")
        #     st.write(fig2)

        st.markdown("### Detailed Data View")
        st.dataframe(df)
        time.sleep(1)