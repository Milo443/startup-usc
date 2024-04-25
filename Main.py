import streamlit as st
import account

from services import initialize_fb
import home
import config_page

config_page.pages_config()
initialize_fb.initialize()

logo_url = ('img\logo.png')
add_images = st.sidebar.image(logo_url)
account.app()

#st.button(on_click=)

