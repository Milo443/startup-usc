import streamlit as st
import json
from controller import controller


logo_url = ('resource\img\logo.png')
add_images = st.sidebar.image(logo_url)




def login_register():
    st.title('Bienvenido a StartUp USC')
    choice = st.selectbox('Login/Signup',['Login', 'Sign Up'])

    if choice == 'Login':
        
        email=st.text_input('Correo Electronico')
        #password = st.text_input('Contraseña', type='password')
    

        st.button('Login', on_click=controller.login(email))

    else:
        email=st.text_input('Correo Electronico')
        password = st.text_input('Contraseña', type='password')
        username = st.text_input('Ingresa nombre de usuario')

        if st.button('Register'):
            controller.register(email,password,username)




