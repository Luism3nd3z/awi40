import web # libreria para usar el framework web.py
import pyrebase # libreria para contecarse con firebase
import firebase_config as token # archivo con la configuracion de firebase
import json # libreria para manejar el formato JSON

app = web.application(urls, globals()) 
render = web.template.render('mvc/views/public/', base="layout")

class Login: 
    def GET(self): 
        try: 
            message = None 
            return render.login(message)
        except Exception as error: # error
            message = "Error en el sistema" 
            print("Error Login.GET: {}".format(error))
            return render.login(message) 

    def POST(self): 
        try: 
            firebase = pyrebase.initialize_app(token.firebaseConfig) 
            auth = firebase.auth() 
            db = firebase.database()
            formulario = web.input() 
            email = formulario.email 
            password= formulario.password 
            print(email,password) 
            user = auth.sign_in_with_email_and_password(email, password) 
            local_id =  (user ['localId'])
            print(local_id) 
            web.setcookie('localid', local_id)
            busqueda =  db.child("usuarios").child(user['localId']).get()
            if busqueda.val()['nivel'] == 'Administrador':
                return web.seeother("/bienvenida_administrador")
            else:
                return web.seeother("/bienvenida_usuario")
            if busqueda.val()['status'] =='activo':
                 return web.seeother("/bienvenida_usuario")
            else:
                return web.seeother("/")

        except Exception as error: # Error en formato JSON
            formato = json.loads(error.args[1])
            error = formato['error'] 
            message = error['message']
            if message == "invalid_password" :
                return render.login(message) 
            print("Error Login.POST: {}".format(message)) 