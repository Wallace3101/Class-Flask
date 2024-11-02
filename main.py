from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3306/dbEjemplo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'

with app.app_context():
    db.create_all()

@app.route("/")
def welcome():
    return render_template("welcome.html")

@app.route("/usuario/registrar")
def usuario_registrar():
    return render_template("registroUsuario.html")

@app.route("/usuario/guardar", methods=["POST"])
def usuario_guardar():
    email = request.form["email"]
    password = request.form["password"]
    new_user = User(email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('usuario_mostrar'))

@app.route("/usuario/mostrar")
def usuario_mostrar():
    usuarios = User.query.all()
    return render_template("mostrarUsuario.html", usuarios=usuarios)

if __name__ == '__main__':
    app.run(debug=True)
