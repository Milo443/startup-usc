import streamlit as st
from pag import home, account 
from services import initialize_fb
import config_page

config_page.pages_config()
initialize_fb.initialize()

add_images = st.sidebar.image('img\logo.png')
account.app()
