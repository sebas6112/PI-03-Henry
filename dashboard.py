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
    page_title="FTX Dashboard",
    page_icon="📊",
    layout="wide",
)

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
st.markdown("<h1 style='text-align: center; color: withe;'>Reporte de los mercados FTX</h1>", unsafe_allow_html=True)
st.write('***')

# Se crean 3 contenedores: el primero y tercero que se actualizan y el de la mitad que es estático y contiene los filtros
placeholder1 = st.empty()
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
        fin_mercado_fecha  = st.date_input("Fecha de inicio",
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

    # Lectura de los datos con los mercados que nos interesan
    df = request.actual_data()
    df = df[df.name.isin(markets_to_use)]
    df.reset_index(drop=True, inplace=True)

    # se inicia y "llena" el contenedor que lleva los valores de los mercados
    with placeholder1.container():
        st.header("Valor y variación de los mercados elegidos")

        # se crea la primera fila de 5 columnas para la mitad del valor de los mercados
        m1, m2, m3, m4, m5 = st.columns(5)
        var_m1 = [m1, m2, m3, m4, m5]
        k = 0
        # se configura cada columna con los valores del dataframe teniendo como referencia la
        # lista market_to_use, si se cambia la lista estos valores cambian automáticamente
        for j in var_m1:
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
        var_m2 = [m1, m2, m3, m4, m5]
        for j in var_m2:
            i = df.index[(df['name'] == markets_to_use[k])].tolist()[0]
            j.metric(
                label = df['name'][i],
                value = df['bid'][i],
                delta = f"{round(df['change24h'][i]*100,2)}%",
            )
            k += 1

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
                        label = df['name'][0],
                        value = df['bid'][0],
                        delta = f"{round(df['change24h'][0]*100,2)}%",
        )
            c2 = st.container()
            c2.metric(
                        label = df['name'][1],
                        value = df['bid'][1],
                        delta = f"{round(df['change24h'][1]*100,2)}%",
        )
        time.sleep(1)
        