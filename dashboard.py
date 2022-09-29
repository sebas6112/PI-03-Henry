from turtle import width
import matplotlib.pyplot as plt  # para gráficas
import seaborn as sns  # para gráficas
import Acquisition.request as request # funciones para conectarse a la api
import time  # para simular datos en tiempo real(?)
import numpy as np  # análisis de datos
import pandas as pd  # manipulación de datos
import plotly.graph_objects as go
import plotly.express as px  # gráficos interactivos
import streamlit as st  # 🎈 desarrollador de páginas web
from plotly.subplots import make_subplots

# Se configura la página
st.set_page_config(
    page_title="FTX Dashboard",
    page_icon="📊",
    layout="wide",
)

# Lista de mercados que nos interesan
markets_to_use = ['BTC/USD', 'ETH/USD', 'USDT/USD', 'BNB/USD', 'XRP/USD', 'SOL/USD', 'DOGE/USD', 'DOT/USD', 'DAI/USD', 'MATIC/USD']

# importamos un df de prueba para la gráfica de velas
df2 = request.historical('BTC/USD',2022,9,28,3600)

# Título del dashboard
st.title("Reporte de los mercados FTX")
st.write('***')

# Se crea el contenedor de los datos que se actializan
placeholder = st.empty()

# Actualización de los datos en "tiempo real"
for seconds in range(30):
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
                delta = f"{round(df['change24h'][i]*100,2)}%",
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
                delta = f"{round(df['change24h'][i]*100,2)}%",
            )
            k += 1

        # create two columns for charts
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("### Ay no sé")
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True,vertical_spacing=0.09,row_heights = [0.85,0.15])

            # fig.add_trace(go.Candlestick(x = df2.index.values,
            #                              open=df2['open'],
            #                              high=df2['high'],
            #                              low=df2['low'],
            #                              close=df2['close']))

            # fig.add_trace(go.Bar(x = df2.index.values, 
            #                      y = df2['volume'], 
            #                      showlegend=False),
            #                                       row=2,
            #                                       col=1)

            # fig.update_layout(autosize = True,
            #                   width = 1000,
            #                   height = 600,
            #                   margin = dict(
            #                                 l = 20,
            #                                 r = 20,
            #                                 b = 0,
            #                                 t = 0,
            #                                 pad = 4
            #                                 )
            #                                 )
            # st.write(fig)
            
        # with fig_col2:
        #     st.markdown("### Second Chart")
        #     fig2 = px.histogram(data_frame=df, x="age_new")
        #     st.write(fig2)

        # st.markdown("### Detailed Data View")
        # st.dataframe(df)
        time.sleep(1)