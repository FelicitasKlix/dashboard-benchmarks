""" 

 """
# streamlit_app.py

import pickle
from pathlib import Path

import streamlit as st
#import streamlit_authenticator as stauth

from views.dashboard import dashboard
from views.dispositivos import dispositivos
#from views.objetivos import objetivos


def main(): 

    with st.sidebar:
        #st.sidebar.title("Welcome {name}")
        st.header("Dashboard Benchmarks")
        api_options = ("Dashboard", "Dispositivos", "Objetivos")
        selected_api = st.selectbox(
            label="Choose your preferred view:",
            options=api_options,
        )

    if(selected_api == "Dashboard"):
        dashboard()
    elif(selected_api == "Dispositivos"):
        dispositivos()


if __name__ == "__main__":
    main()