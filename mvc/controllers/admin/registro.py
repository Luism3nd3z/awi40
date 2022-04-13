import web # libreria para usar el framework web.py
import pyrebase # libreria para contecarse con firebase
import firebase_config as token # archivo con la configuracion de firebase
import json # libreria para manejar el formato JSON

app = web.application(urls, globals()) 
render = web.template.render('mvc/controllers/admin/', base="layout")



class Registro:
    def GET(self): 
        try: 
            message = None 
            return render.registro(message) 
        except Exception as error: 
            message = "Error en el sistema" 
            print("Error registro.GET: {}") 
            return render.registro(message) 


    def POST(self): 
        try: 
            firebase = pyrebase.initialize_app(token.firebaseConfig) 
            auth = firebase.auth() 
            db = firebase.database() 
            formulario = web.input() 
            name= formulario.name
            phone= formulario.phone
            email = formulario.email 
            password= formulario.password 
            nivel= formulario.nivel
            user = auth.create_user_with_email_and_password(email,password)  
            local_id =  (user ['localId'])
            data = {
            "name": name,
            "phone": phone,
            "email": email,
            "nivel": nivel
            }
            results = db.child("usuarios").child(user['localId']).set(data)
            return web.seeother("/") 
        except Exception as error: 
            formato = json.loads(error.args[1]) # Error en formato JSON
            error = formato['error'] 
            message = error['message']
            print("Error Registro.POST: {}".format(message)) 
            web.setcookie('localID', None, 3600) 
            return render.registro(message) 