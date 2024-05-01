import streamlit as st
import json
from controller import controller


logo_url = ('resource\img\logo.png')
add_images = st.sidebar.image(logo_url)



#---------------seccion de login y registro----------------
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


def create_company():
    st.title('Crea un nombre atractivo para tu compañia:')
    name_company = st.text_input('Nombre de tu compañia')
    your_logo=st.file_uploader ('Carga el logo de tu compañia',type=["png", "jpg", "jpeg"])
    if your_logo is not None:
        controller.uploader(your_logo)
    st.button('Next')

#login_register()
create_company()

#moises es un perro