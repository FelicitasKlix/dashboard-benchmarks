import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery
import pandas as pd



# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)

print(credentials)

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.


def usersQuery():
    @st.cache_data(ttl=600)
    def run_query(query):
        query_job = client.query(query)
        result = query_job.result()
        df = next(result)[0] if result.total_rows > 0 else 0
        return df

    users = run_query("SELECT COUNT(DISTINCT user_pseudo_id) FROM `" + credentials.project_id + ".analytics_350643411.events_2023*` WHERE traffic_source.name LIKE 'RX_%'")
    
    return users

def eventsQuery():
    @st.cache_data(ttl=600)
    def run_query(query):
        query_job = client.query(query)
        df = query_job.to_dataframe()
        #result = query_job.result()
        return df.to_dict(orient='records')
    
    events = run_query("SELECT event_name, COUNT(event_name) FROM `" + credentials.project_id + ".analytics_350643411.events_2023*` WHERE (event_name LIKE 'GA4 - Zoho lead success' or event_name LIKE '%GA4 - Sign up%' or event_name LIKE 'GA4 - Zoho lead sent') AND traffic_source.name LIKE 'RX_%' GROUP BY event_name")

    return events

@st.cache_data(ttl=600)
def global_data():
    query = "SELECT DISTINCT traffic_source.name, event_name, COUNT(event_name) FROM `" + credentials.project_id + ".analytics_350643411.events_2023*` WHERE traffic_source.name LIKE 'RX_%' AND (event_name LIKE 'GA4 - Zoho lead success' or event_name LIKE '%GA4 - Sign up%' or event_name LIKE 'GA4 - Zoho lead sent') GROUP BY traffic_source.name, event_name"
    query_job = client.query(query)
    df = query_job.to_dataframe()
    return df

@st.cache_data(ttl=600)
def device_data():
    query = "SELECT DISTINCT event_date, device.category, traffic_source.name, event_name, COUNT(event_name) FROM `" + credentials.project_id + ".analytics_350643411.events_2023*` WHERE (event_name LIKE 'GA4 - Zoho lead success' or event_name LIKE 'GA4 - Sign up' or event_name LIKE 'GA4 - Zoho lead sent') AND traffic_source.name LIKE 'RX_%' GROUP BY event_date, device.category, traffic_source.name, event_name ORDER BY event_date ASC"
    query_job = client.query(query)
    df = query_job.to_dataframe()
    return df

@st.cache_data(ttl=600)
def global_data_benchmarks():
    query = "SELECT * FROM `" + credentials.project_id + ".registro_clientes.registro_data`"
    query_job = client.query(query)
    df = query_job.to_dataframe()
    return df

@st.cache_data(ttl=600)
def global_media_benchmarks():
    query = "SELECT * FROM `" + credentials.project_id + ".registro_clientes.registro_media`"
    query_job = client.query(query)
    df = query_job.to_dataframe()
    return df

@st.cache_data(ttl=600)
def get_industrias():
    query = "SELECT DISTINCT industria FROM `" + credentials.project_id + ".registro_clientes.registro_data`"
    query_job = client.query(query)
    df = query_job.to_dataframe()
    #hacer una lista de industrias en base a la respuesta de la query
    industrias = df["industria"].tolist()
    return industrias

@st.cache_data(ttl=600)
def get_tipo_cliente():
    query = "SELECT DISTINCT tipo_cliente FROM `" + credentials.project_id + ".registro_clientes.registro_data`"
    query_job = client.query(query)
    df = query_job.to_dataframe()
    #hacer una lista de tipo de cliente en base a la respuesta de la query
    tipo_clientes = df["tipo_cliente"].tolist()
    return tipo_clientes

@st.cache_data(ttl=600)
def get_objetivo_campaña():
    query = "SELECT DISTINCT objetivo_campaña FROM `" + credentials.project_id + ".registro_clientes.registro_data`"
    query_job = client.query(query)
    df = query_job.to_dataframe()
    #hacer una lista de tipo de cliente en base a la respuesta de la query
    objetivos_campaña = df["objetivo_campaña"].tolist()
    return objetivos_campaña

@st.cache_data(ttl=600)
def get_tipo_campaña():
    query = "SELECT DISTINCT tipo_campaña FROM `" + credentials.project_id + ".registro_clientes.registro_data`"
    query_job = client.query(query)
    df = query_job.to_dataframe()
    #hacer una lista de tipo de campaña en base a la respuesta de la query
    objetivos_campaña = df["tipo_campaña"].tolist()
    return objetivos_campaña

@st.cache_data(ttl=600)
def get_paises():
    query = "SELECT DISTINCT pais FROM `" + credentials.project_id + ".registro_clientes.registro_data`"
    query_job = client.query(query)
    df = query_job.to_dataframe()
    #hacer una lista de paises en base a la respuesta de la query
    paises = df["pais"].tolist()
    return paises

@st.cache_data(ttl=600)
def get_anios():
    query = "SELECT DISTINCT year FROM `" + credentials.project_id + ".registro_clientes.registro_data` ORDER BY year ASC"
    query_job = client.query(query)
    df = query_job.to_dataframe()
    #hacer una lista de paises en base a la respuesta de la query
    anios = df["year"].tolist()
    return anios