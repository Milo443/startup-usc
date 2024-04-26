import firebase_admin 

from firebase_admin import credentials
from firebase_admin import auth

def initialize():
    #se corre servicio de auth de firebase y se verifica si el servicio ya esta ejecutado o no
    credential = credentials.Certificate('startup-usc-eee3f6cf1d92.json')
    try:
        default_app = firebase_admin.get_app()

    except:
        firebase_admin.initialize_app(credential)