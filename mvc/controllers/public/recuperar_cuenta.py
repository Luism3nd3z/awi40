import web # libreria para usar el framework web.py
import pyrebase # libreria para contecarse con firebase
import firebase_config as token # archivo con la configuracion de firebase
import json # libreria para manejar el formato JSON


app = web.application(urls, globals()) 
render = web.template.render('mvc/views/public/', base="layout")



class Recuperar_cuenta:
    def GET(self): 
           return render.recuperar_cuenta() 

    def POST(self): 
            firebase = pyrebase.initialize_app(token.firebaseConfig) 
            auth = firebase.auth() 
            formulario = web.input() 
            email = formulario.email
            results = auth.send_password_reset_email(email)
            print(results)
