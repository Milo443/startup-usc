import streamlit as st
import json

def pages_config():
    #configuracion basica de la pagina
    st.set_page_config(
        page_title="StartUp USC",
        page_icon="👨‍💼",
        initial_sidebar_state="collapsed",
    )

class usuarios:
    def __init__(self, dato_string):
        self.dato_json = json.loads(dato_string)

    def obtener_email(self):
        return self.dato_json["email"]
    