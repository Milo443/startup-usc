import streamlit as st
import firebase_admin 

from firebase_admin import credentials
from firebase_admin import auth
#import pages.account as account 

credential = credentials.Certificate('startup-usc-eee3f6cf1d92.json')
try:
    default_app = firebase_admin.get_app()

except:
    firebase_admin.initialize_app(credential)

st.set_page_config(
    page_title="StartUp USC",
    page_icon="👨‍💼",
)   

st.title("StartUp Simulator USC")
st.sidebar.success("Selecciona la pagina")

#account.app()