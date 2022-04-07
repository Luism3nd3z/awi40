import pyrebase # libreria para contecarse con firebase
import firebase_config as token # archivo con la configuracion de firebase
 

firebase = pyrebase.initialize_app(token.firebaseConfig)
auth = firebase.auth()
db = firebase.database()
#----1
#leer datos para un usuario
name = input("Nombre: ")
phone = input("Telefono: ")
email = input("Email: ")
password = input("Password: ")

#crear usuario
user = auth.create_user_with_email_and_password(email, password)


#agregar datos de un usuario a base de datos
data = {
    "name": name,
    "phone": phone,
    "email": email
}

#leer datos del usuario
results = db.child("usuarios").child(user['localId']).set(data)

#----2
#recuperar contraseña
email="1720110731@utectulancingo.edu.mx"

results = auth.send_password_reset_email(email)
print(results)
 
'''
#----3

localId = "eHfATztQa5XeTVSFQ1OjuAbj7Z03"
user = db.child("usuarios").child(localId).get()    
if user.val() is None:
    print("redirect to login")
else:
    print("get user info: ", user.val())
    print("get email: ", user.val()['email'])
    print("get name: ", user.val()['name'])

'''