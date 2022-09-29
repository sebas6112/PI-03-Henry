from http.cookies import CookieError
from operator import contains
import seaborn as sns  # para gráficas
import Acquisition.request as request # funciones para conectarse a la api
import time  # para simular datos en tiempo real(?)
import numpy as np  # análisis de datos
import pandas as pd  # manipulación de datos
import plotly.graph_objects as go
import plotly.express as px  # gráficos interactivos
import streamlit as st  # 🎈 desarrollador de páginas web
from plotly.subplots import make_subplots
import datetime
from datetime import datetime

# Se configura la página
st.set_page_config(
    page_title="Análisis Individual",
    page_icon="📊",
    layout="wide",
)

st.sidebar.header("Análisis Individual")

# Lista de mercados que nos interesan
markets_to_use = ['BTC/USD', 'ETH/USD', 'USDT/USD', 'BNB/USD', 'XRP/USD', 'SOL/USD', 'DOGE/USD', 'DOT/USD', 'DAI/USD', 'MATIC/USD']

# Diccionario con el valor (en segundos) de la resolución para las consultas históricas
resolution_dict = {"Cinco minutos":300,
                    "Una hora":3500,
                    "Cuatro horas":14400,
                    "Un día":86400,
                    "Una semana":604800,
                    "Un mes":2592000}

# Título del dashboard
st.markdown("<h1 style='text-align: center; color: withe;'>Análisis de un mercado individual</h1>", unsafe_allow_html=True)
st.write('***')

placeholder2 = st.empty()
placeholder3 = st.empty()

# Se crean los filtros para las consultas a la API, esta columna es estática
# por eso se llena antes de empezar la lectura continua de los datos
with placeholder2.container():

    st.write('***')
    st.header("Análisis por mercado")

    # Se divide el espacio en 5 y distribuyendolo con la configuración de la lista
    m1, m2, m3, m4, m5,m6,m7 = st.columns([2,1,2,1,2,1,2])
    
    # Se crea el filtro para el mercado que se va a trabajar
    with m1:
        mercado_actual = st.selectbox('Elige el mercado que quieras analizar:',
                                markets_to_use)
                                
    # Se crean los filtros para el intervalo del tiempo
    with m3:
        inicio_mercado_fecha = st.date_input("Fecha de inicio",
                                        key = 1,
                                        value = datetime(2022,1,1),
                                        max_value = datetime.now())
    with m5:
        fin_mercado_fecha  = st.date_input("Fecha de Fin",
                                     key=2,
                                     value=datetime.now().date(),
                                     min_value=inicio_mercado_fecha,
                                     max_value=datetime.now())
    # Se convierten los datos de datetime.datetime a un número para enviarle a la API
    inicio_mercado = datetime.combine(inicio_mercado_fecha, datetime.min.time()).timestamp()
    fin_mercado = datetime.combine(fin_mercado_fecha, datetime.min.time()).timestamp()
    
    # Se crea el filtro de la resolución de los datos
    with m7:
        resolution = st.selectbox('Elige la resolución entre muestras',
                                resolution_dict.keys(),index=3)

# Actualización de los datos en "tiempo real"
while True:

    # Se llena el tercer contenedor que tiene las gráficas y valores detallados del mercado elegido en la sección de filtros
    with placeholder3.container():
        # Se crean dos columnas: una grande para alojar la gráfica y otra pequeña para alojar los datos
        col1, col2 = st.columns([3, 1])
        
        # Se consultan los datos históricos con los datos elegidos en los filtros
        df2 = request.historical_datetime(mercado_actual,inicio_mercado,fin_mercado,resolution_dict[resolution])

        # Se llena la columna 1 con la gráfica
        with col1:

            st.subheader(f'Análisis del mercado de {mercado_actual} del {inicio_mercado_fecha} al {fin_mercado_fecha}')
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True,vertical_spacing=0.09,row_heights = [0.85,0.15])

            fig.add_trace(go.Candlestick(x = df2.index.values,
                                         open=df2['open'],
                                         high=df2['high'],
                                         low=df2['low'],
                                         close=df2['close']))

            fig.add_trace(go.Bar(x = df2.index.values, 
                                 y = df2['volume'], 
                                 showlegend=False),
                                                  row=2,
                                                  col=1)

            fig.update_layout(autosize = True,
                              width = 1000,
                              height = 600,
                              margin = dict(
                                            l = 20,
                                            r = 20,
                                            b = 0,
                                            t = 0,
                                            pad = 4
                                            )
                                            )
            st.write(fig)
        with col2:
            c1 = st.container()
            c1.metric(
                        label = 'Mercado Actual',
                        value = df2['open'][0],
        )
            # c2 = st.container()
            # c2.metric(
            #             label = df2['name'],
            #             value = df2['bid'],
            #             delta = f"{round(df2['change24h']*100,2)}%",
        # )
        time.sleep(1)