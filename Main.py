import streamlit as st
import firebase_admin 

from firebase_admin import credentials
from firebase_admin import auth
from streamlit import option_menu

from pages import home, account 

#se corre servicio de auth de firebase y se verifica si el servicio ya esta ejecutado o no
credential = credentials.Certificate('startup-usc-eee3f6cf1d92.json')
try:
    default_app = firebase_admin.get_app()

except:
    firebase_admin.initialize_app(credential)



#configuracion basica de la pagina
st.set_page_config(
    page_title="StartUp USC",
    page_icon="👨‍💼",
)   

class MultiApp:
    def __init__(self):
        self.app == []
    def add_app(self, title, function):
        self.apps.append({
            "tittle":title,
            "function": function
        })

def run():
    with st.sidebar:
        app = option_menu(
            menu_title='StartUp USC',
            options=['home','account'],
            icons=['house-fill','person-circle'],
            menu_icon = 'chat-text-fill',
            default_index = 1,
            styles={
                "container": {"padding": "5!important","background-color":'black'},
        "icon": {"color": "white", "font-size": "23px"}, 
        "nav-link": {"color":"white","font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "blue"},
        "nav-link-selected": {"background-color": "#02ab21"},
            }
        )
        if app == "Home":
            home.app()
        if app == "Account":
            account.app()    
