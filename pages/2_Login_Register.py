import streamlit as st
import firebase_admin 

from firebase_admin import credentials
from firebase_admin import auth

#credential = credentials.Certificate('startup-usc-eee3f6cf1d92.json')
#firebase_admin.initialize_app(credential)



def app():
    st.title('Bienvenido a StartUp USC')
    choice = st.selectbox('Login/Signup',['Login', 'Sign Up'])

    def f():
            #user = auth.get_user_by_email(email)
            #st.success('Login Exitoso')
            try:
                # Obtener el usuario por correo electrónico
                user = auth.get_user_by_email(email)
                
                
                 # Verificar la contraseña
                expiry_duration = 3600000  # 1 hora en milisegundos
                id_token = auth.create_session_cookie(user.uid, password, expires_in=expiry_duration)
                decoded_token = auth.verify_id_token(id_token)
                uid = decoded_token['uid']

                if decoded_token:
                    st.success(f'Login Exitoso para el usuario con UID: {uid}')
                else:
                    st.warning('La contraseña es incorrecta.')
                    
            except auth.UserNotFoundError:
                st.warning('El correo electrónico no está registrado.')
            except Exception as e:
                st.warning(f'Error: {e}')



    if choice == 'Login':
        
        email=st.text_input('Correo Electronico')
        password = st.text_input('Contraseña', type='password')
        
        st.button('Login', on_click=f)

    else:
        email=st.text_input('Correo Electronico')
        password = st.text_input('Contraseña', type='password')
        username = st.text_input('Ingresa nombre de usuario')

        if st.button('Register'):
            try:
                user = auth.create_user(email=email, password=password, uid=username)
                st.success('Cuenta creada con exito')
                st.markdown('Porfavor logueate usando tu correo y contrasena')
                st.balloons()
            except Exception as e:
                st.warning(f'Error: {e}')

app() 


