#dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

#from charts.funnel import render_custom_funnel
from queries.queries import usersQuery, eventsQuery, global_data, global_data_benchmarks, global_media_benchmarks, get_industrias, get_tipo_cliente, get_objetivo_campaña, get_tipo_campaña, get_paises, get_anios


def  dashboard():
    users = usersQuery()
    eventos= eventsQuery()
    tofl = eventos[2]["f0_"]
    zl_sent = eventos[0]["f0_"]
    zl_success = eventos[1]["f0_"]
    df_data = global_data_benchmarks()
    df_media = global_media_benchmarks()
    industrias = get_industrias()
    tipos_clientes = get_tipo_cliente()
    #objetivos = get_objetivo_campaña()
    #tipos_campaña = get_tipo_campaña()
    paises = get_paises()
    anios = get_anios()
    

    year_start = datetime.date(anios[0], 1, 1)
    year_end = datetime.date(anios[-1], 12, 31)
    today = datetime.datetime.now()
    #year_start = datetime.date(today.year, 1, 1)
    #year_end = datetime.date(today.year, 12, 31)
    months = {"Enero":"1", "Febrero":"2", "Marzo":"3", "Abril":"4", "Mayo":"5", "Junio":"6", "Julio":"7", "Agosto":"8", "Septiembre":"9", "Octubre":"10", "Noviembre":"11", "Diciembre":"12"}

    # Dividir la pantalla en dos columnas para los select box
    left_column, right_column = st.columns(2)

    with left_column:
        # Establece el rango del año corriente
        date_range = st.date_input(
            "Select date range",
            (year_start, year_end),  # Establece las fechas de inicio y fin del año corriente
            year_start,  # Establece la fecha de inicio predeterminada
            year_end,    # Establece la fecha de fin predeterminada
            format="MM.DD.YYYY",
        )
        # # Establece el rango del año corriente
        # first_column, second_column = st.columns(2)
        # with first_column:
        #     start_year = st.selectbox("Select start year", ["All"] + anios)
        # with second_column:
        #     end_year = st.selectbox("Select end year", ["All"] + anios)
    

    with right_column:
        #country = st.selectbox("Select country", ["All"] + paises)
        # Establece el rango del año corriente
        first_column, second_column = st.columns(2)
        with first_column:
            start_month = st.selectbox("Select start year", months.keys())
        with second_column:
            end_month = st.selectbox("Select end year", months.keys())

    # Dividir la pantalla en dos columnas para los select box
    left_column, right_column = st.columns(2)

    # Agregar filtro desplegable para la categoría (mobile, desktop, tablet)
    with left_column:
        ind = st.selectbox("Select Industria", ["All"] + industrias)

    # Agregar filtro desplegable para el país
    with right_column:
        tipo_cl = st.selectbox("Select Tipo de Cliente", ["All"] + tipos_clientes)

     # Dividir la pantalla en dos columnas para los select box
    left_column, right_column = st.columns(2)

    # Agregar filtro desplegable para la categoría (mobile, desktop, tablet)
    with left_column:
        obj = st.selectbox("Select Tipo de Campaña", ["All"] )

    # Agregar filtro desplegable para el país
    with right_column:
        tipo_camp = st.selectbox("Select Medio", ["All"] )

    st.title("Registro Data")
    st.write(year_start)
    st.write(year_end)
    st.write(date_range[0].year, date_range[0].month)
    st.write(date_range[1].year, date_range[1].month)
    #st.dataframe(df_data, use_container_width=True)
    # if(ind == "All" and tipo_cl == "All" and obj == "All" and tipo_camp == "All"):
    #     filtered_df = df_data
    # elif(ind != "All" and tipo_cl == "All" and obj == "All" and tipo_camp == "All"):
    #     filtered_df = df_data[df_data['industria'] == ind]
    # elif(ind == "All" and tipo_cl != "All" and obj == "All" and tipo_camp == "All"):
    #     filtered_df = df_data[df_data['tipo'] == tipo_cl]
    # elif(ind == "All" and tipo_cl == "All" and obj != "All" and tipo_camp == "All"):
    #     filtered_df = df_data[df_data['objetivo'] == obj]
    # elif(ind == "All" and tipo_cl == "All" and obj == "All" and tipo_camp != "All"):
    #     filtered_df = df_data[df_data['tipo_camp'] == tipo_camp]
    # elif(ind != "All" and tipo_cl != "All" and obj == "All" and tipo_camp == "All"):
    #     filtered_df = df_data[(df_data['industria'] == ind) & (df_data['tipo'] == tipo_cl)]
    # elif(ind != "All" and tipo_cl == "All" and obj != "All" and tipo_camp == "All"):
    #     filtered_df = df_data[(df_data['industria'] == ind) & (df_data['objetivo'] == obj)]
    # elif(ind != "All" and tipo_cl == "All" and obj == "All" and tipo_camp != "All"):
    #     filtered_df = df_data[(df_data['industria'] == ind) & (df_data['tipo_camp'] == tipo_camp)]
    # elif(ind == "All" and tipo_cl != "All" and obj != "All" and tipo_camp == "All"):
    #     filtered_df = df_data[(df_data['tipo'] == tipo_cl) & (df_data['objetivo'] == obj)]

    #else:
        #filtered_df = df_data[(df_data['industria'] == ind) & (df_data['tipo_cliente'] == tipo_cl)& (df_data['objetivo_campaña'] == obj) & (df_data['tipo_campaña'] == tipo_camp)]
    
    #filtered_df = df_data[df_data['industria'] == category]
    #st.dataframe(filtered_df, use_container_width=True)

    # Filtrar el DataFrame en base a los filtros seleccionados
    filtered_df = df_data[
        (df_data['year'] >= date_range[0].year) & (df_data['year'] <= date_range[1].year)
    ]

    st.dataframe(filtered_df, use_container_width=True)

    st.title("Registro Media")
    st.dataframe(df_media, use_container_width=True)

    # st.title("FUNNEL")
    # render_custom_funnel(users, tofl, zl_sent, zl_success)

    # st.title("Table")
    # metricas = pd.DataFrame(eventos)

    # users_row = pd.DataFrame({"event_name": ["users"], "f0_": [users]})
    # metricas = pd.concat([users_row, metricas], ignore_index=True)
    # conv0_row = pd.DataFrame({"event_name": ["Conv0"], "f0_": [(tofl/users)*100]})
    # metricas = pd.concat([metricas, conv0_row], ignore_index=True)
    # conv1_row = pd.DataFrame({"event_name": ["Conv1"], "f0_": [(zl_success/tofl)*100]})
    # metricas = pd.concat([metricas, conv1_row], ignore_index=True)
    # conv12_row = pd.DataFrame({"event_name": ["Conv1/2"], "f0_": [(zl_success/zl_sent)*100]})
    # metricas = pd.concat([metricas, conv12_row], ignore_index=True)
    
    # st.dataframe(metricas)


    # st.title("Funnel")
    # eventos_funnel = pd.DataFrame(eventos)
    # eventos_funnel = pd.concat([users_row, eventos_funnel], ignore_index=True)

    # # Supongamos que 'df' es tu DataFrame con los datos
    # #data = eventos_funnel[eventos_funnel['event_name'].isin(['users', 'GA4 - Sign up', 'GA4 - Zoho lead sent', 'GA4 - Zoho lead success'])]

    # # Crea un diccionario con los datos adecuados para el gráfico
    # data_dict = {
    #     'number': eventos_funnel['f0_'],
    #     'stage': eventos_funnel['event_name']
    # }

    # # Crea el gráfico de embudo
    # fig = px.funnel(data_dict, x='number', y='stage')

    # # Muestra el gráfico
    # #fig.show()
    # st.plotly_chart(fig, use_container_width=True)