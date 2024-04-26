import streamlit as st
from streamlit_router import StreamlitRouter
import json
from controller import controller

router = StreamlitRouter()

buttonp=st.button("prueba")
buttons=st.button("salir")



def login_register():
    st.title('Bienvenido a StartUp USC')
    choice = st.selectbox('Login/Signup',['Login', 'Sign Up'])

    if choice == 'Login':
        
        email=st.text_input('Correo Electronico')
        #password = st.text_input('Contraseña', type='password')
    

        st.button('Logina', on_click=controller.login(email))

    else:
        email=st.text_input('Correo Electronico')
        password = st.text_input('Contraseña', type='password')
        username = st.text_input('Ingresa nombre de usuario')

        if st.button('Register'):
            controller.register(email,password,username)

def salir():
    st.title('salirC')
    choice = st.selectbox('Login/Signup',['Login', 'Sign Up'])   


router.register(login_register(), "/Login_Register")
router.register(salir(), "/salir")

def botones():
    if buttonp:
        try:
            router.redirect(router.build("/Login_Register"))
        except KeyError:
            st.error("La ruta '/Login_Register' no está registrada correctamente.")
        #except AttributeError:
            #st.error("La ruta '/Login_Register' no está registrada correctamente.")
    #router.run()
    if buttons:
        try:
            router.redirect(router.build("/salir"))
        except KeyError:
            st.error("La ruta '/Login_Register' no está registrada correctamente.")








