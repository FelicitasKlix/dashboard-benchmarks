#dispositivos.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import datetime
#from streamlit_echarts import st_echarts


from queries.queries import device_data

def dispositivos():
    st.title("Dispositivos")
    today = datetime.datetime.now()
    year_start = datetime.date(today.year, 1, 1)
    year_end = datetime.date(today.year, 12, 31)

    # Establece el rango del año corriente
    date_range = st.date_input(
        "Select date range",
        (year_start, year_end),  # Establece las fechas de inicio y fin del año corriente
        year_start,  # Establece la fecha de inicio predeterminada
        year_end,    # Establece la fecha de fin predeterminada
        format="MM.DD.YYYY",
    )

    # Dividir la pantalla en dos columnas para los select box
    left_column, right_column = st.columns(2)

    # Agregar filtro desplegable para la categoría (mobile, desktop, tablet)
    with left_column:
        category = st.selectbox("Select category", ["All","mobile", "desktop", "tablet"])

    # Agregar filtro desplegable para el país
    with right_column:
        #country_options = ["All", "México", "Colombia", "Brasil", "Perú", "Argentina", "Ecuador", "Costa Rica", "Chile"]
        country_options = {"All":"All", "México": "_MX_", "Colombia": "_CO_", "Brasil": "_BR_", "Perú": "_PE_", "Argentina": "_AR_", "Ecuador": "_EC_", "Costa Rica": "_CR_", "Chile": "_CL_"}
        country = st.selectbox("Select country", country_options.keys())
    

    df = device_data()

    if len(date_range)==2 and date_range[1] is not None:
        # Convierte las fechas en formato 20230822
        start_date = date_range[0].strftime('%Y%m%d')
        end_date = date_range[1].strftime('%Y%m%d')

        if category == "All" and country == "All":
            # Muestra todos los valores sin ningún filtro
            filtered_df = df[(df['event_date'] >= start_date) & (df['event_date'] <= end_date)]
        elif category == "All":
            # Filtra por país y rango de fechas
            filtered_df = df[(df['event_date'] >= start_date) & (df['event_date'] <= end_date) & df['name'].str.contains(country_options[country])]
        elif country == "All":
            # Filtra por categoría y rango de fechas
            filtered_df = df[(df['event_date'] >= start_date) & (df['event_date'] <= end_date) & (df['category'] == category)]
        else:
            # Filtra por categoría, país y rango de fechas
            filtered_df = df[(df['event_date'] >= start_date) & (df['event_date'] <= end_date) & (df['category'] == category) & df['name'].str.contains(country_options[country])]
    else:
        # Si no se selecciona un end_date, muestra el DataFrame sin filtrar
        filtered_df = df



    st.dataframe(filtered_df, hide_index=True, use_container_width=True)

    st.title("Por Dispositivo")
    # Define un orden personalizado para las categorías de dispositivos
    category_order = ['mobile', 'desktop', 'tablet']
    # Filtra el DataFrame original para las categorías especificadas en el orden deseado
    filtered_df = filtered_df[filtered_df['category'].isin(category_order)]
    # Reorganiza los datos
    #pivot_df = filtered_df.pivot(index='event_date', columns='event_name', values='f0_')
    pivot_df = filtered_df.groupby(['category', 'event_name'])['f0_'].sum().unstack().reset_index()


    # Crea el gráfico
    fig = go.Figure()

    for event_name in ['GA4 - Sign up', 'GA4 - Zoho lead success', 'GA4 - Zoho lead sent']:
        fig.add_trace(go.Funnel(
            name=event_name,
            y=pivot_df['category'],
            x=pivot_df[event_name])
        )

    fig.update_layout(
                    xaxis_title="Event Count",
                    yaxis_title="Device Category",
                    width=800,
                    height=500)

    st.plotly_chart(fig, use_container_width=False)

    st.title("Por Plataforma")
    event = st.selectbox("Select event", ["All",'GA4 - Sign up', 'GA4 - Zoho lead success', 'GA4 - Zoho lead sent'])
    if event == "All":
        filtered_fb_df = filtered_df[filtered_df['name'].str.contains('_FB_')]
        filtered_go_df = filtered_df[filtered_df['name'].str.contains('_GO_')]
    else:
        # Filtrar para la plataforma de Facebook (_FB_)
        filtered_fb_df = filtered_df[filtered_df['name'].str.contains('_FB_') & (filtered_df['event_name'] == event)]
        # Filtrar para la plataforma de Google (_GO_)
        filtered_go_df = filtered_df[filtered_df['name'].str.contains('_GO_') & (filtered_df['event_name'] == event)]

    # Dividir la pantalla en dos columnas
    col1, col2 = st.columns(2)

    # Crear un gráfico de torta para la plataforma de Facebook en la primera columna
    with col1:
        fig_fb = px.pie(filtered_fb_df, names='category', title='Plataforma de Facebook')
        st.plotly_chart(fig_fb, use_container_width=True)

    # Crear un gráfico de torta para la plataforma de Google en la segunda columna
    with col2:
        fig_go = px.pie(filtered_go_df, names='category', title='Plataforma de Google')
        st.plotly_chart(fig_go, use_container_width=True)

    # # Crear un gráfico de torta para la plataforma de Facebook
    # fig_fb = px.pie(filtered_fb_df, names='category', title='Plataforma de Facebook')
    
    # # Crear un gráfico de torta para la plataforma de Google
    # fig_go = px.pie(filtered_go_df, names='category', title='Plataforma de Google')

    # st.plotly_chart(fig_fb, use_container_width=True)
    # st.plotly_chart(fig_go, use_container_width=True)