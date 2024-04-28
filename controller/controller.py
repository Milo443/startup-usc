import streamlit as st
import firebase_admin
import json

from firebase_admin import credentials
from firebase_admin import auth

from models import initialize_fb


#credential = credentials.Certificate('startup-usc-eee3f6cf1d92.json')
#firebase_admin.initialize_app(credential)

#config_page.pages_config()
initialize_fb.initialize()

def pages_config():
    #configuracion basica de la pagina
    st.set_page_config(
        page_title="StartUp USC",
        page_icon="👨‍💼",
        initial_sidebar_state="collapsed",
    )

def login(email):   
    try:
        user = auth.get_user_by_email(email=email)
        # Obtener el usuario por correo electrónico
        st.success('Login Exitoso')
        p = st.session_state.authenticated = True
        #st.success(p)
    except auth.UserNotFoundError:
        st.warning('El correo electrónico no está registrado.')
    except Exception as e:
        st.warning(f'Error: {e}')

def register(email,password,username):
        try:
            user = auth.create_user(email=email, password=password, uid=username)
            st.success('Cuenta creada con exito')
            st.markdown('Porfavor logueate usando tu correo y contrasena')
            st.balloons()
        except Exception as e:
            st.warning(f'Error: {e}')

def uploader(your_logo):
            st.image(your_logo,width=100)
