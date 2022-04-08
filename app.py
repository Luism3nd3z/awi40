import web # libreria para usar el framework web.py
import pyrebase # libreria para contecarse con firebase
import firebase_config as token # archivo con la configuracion de firebase
import json # libreria para manejar el formato JSON

urls = (
    '/', 'Login',
    '/registro', 'Registro',
    '/bienvenida', 'Bienvenida',
    '/logout', 'Logout',
    '/sensor', 'Sensor',
    '/recuperar_cuenta', 'Recuperar_cuenta',
    '/users_list','UsersList',
    '/user_view/(.*)','Userview',
)
app = web.application(urls, globals()) 
render = web.template.render('views/', base="layout")

class Inicio:
    def GET(self): 
        return render.recuperar_cuenta() 


class Userview:                             
    def GET(self,localId):
        try:
            firebase = pyrebase.initialize_app(token.firebaseConfig) 
            db = firebase.database() 
            user =  db.child("usuarios").child(localId).get()
            return render.user_view(user) 
        except Exception as error: 
            print("Error Userview.GET: {}".format(error))

class UsersList:                             
    def GET(self):
        try:
            firebase = pyrebase.initialize_app(token.firebaseConfig) 
            db = firebase.database() 
            users = db.child("usuarios").get()
            return render.users_list(users) 
        except Exception as error: 
            print("Error UsersList.GET: {}".format(error))

 

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

    
class Logout:
    def GET(self):
        web.setcookie('localid', None) # valor none 
        return web.seeother("/") # redirecinar a login

class Bienvenida:
    def GET(self): 
        if ( web.cookies().get('localid')) != "": # cookie
            return render.bienvenida() # redirecinar a bienevenida
        else:
            return render.login() # redirecinar a login

    
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
            formulario = web.input() 
            email = formulario.email 
            password= formulario.password 
            print(email,password) 
            user = auth.sign_in_with_email_and_password(email, password) 
            local_id =  (user ['localId'])
            print(local_id)  
            web.setcookie('localid', local_id)
            return web.seeother("bienvenida")
        except Exception as error: # Error en formato JSON
            formato = json.loads(error.args[1])
            error = formato['error'] 
            message = error['message']
            if message == "invalid_password" :
                return render.login(message) 
            print("Error Login.POST: {}".format(message)) 

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
            user = auth.create_user_with_email_and_password(email,password)  
            local_id =  (user ['localId'])
            data = {
            "name": name,
            "phone": phone,
            "email": email
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

if __name__ == "__main__":
    web.config.debug = True





