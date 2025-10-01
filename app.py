import os
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Cargar variables de entorno desde un archivo .env
load_dotenv()

#crear instancia
app =  Flask(__name__)

# Configuración de la base de datos PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#Modelo de la base de datos
class Empleado(db.Model):
    __tablename__ = 'empleados'
    no_empleado = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String)
    ap_paterno = db.Column(db.String)
    ap_materno = db.Column(db.String)
    departamento = db.Column(db.String)
    puesto = db.Column(db.String)

    def to_dict(self):
        return{
            'no_empleado': self.no_empleado,
            'nombre': self.nombre,
            'ap_paterno': self.ap_paterno,
            'ap_materno': self.ap_materno,
            'departamento': self.departamento,
            'puesto': self.puesto,
        }

#Ruta raiz
@app.route('/')
def index():
    empleados = Empleado.query.all()
    return render_template('index.html', empleados=empleados)

#Ruta /empleados crear un nuevo empleado
@app.route('/empleados/new', methods=['GET','POST'])
def create_empleado():
    if request.method == 'POST':
        no_empleado = request.form['no_empleado']
        nombre = request.form['nombre']
        ap_paterno = request.form['ap_paterno']
        ap_materno = request.form['ap_materno']
        departamento = request.form['departamento']
        puesto = request.form['puesto']

        nvo_empleado = Empleado(
            no_empleado=no_empleado,
            nombre=nombre,
            ap_paterno=ap_paterno,
            ap_materno=ap_materno,
            departamento=departamento,
            puesto=puesto
        )

        db.session.add(nvo_empleado)
        db.session.commit()

        return redirect(url_for('index'))
    
    return render_template('create_empleado.html')

#Eliminar empleado
@app.route('/empleados/delete/<string:no_empleado>')
def delete_empleado(no_empleado):
    empleado = Empleado.query.get(no_empleado)
    if empleado:
        db.session.delete(empleado)
        db.session.commit()
    return redirect(url_for('index'))

#Actualizar empleado
@app.route('/empleados/update/<string:no_empleado>', methods=['GET','POST'])
def update_empleado(no_empleado):
    empleado = Empleado.query.get(no_empleado)
    if request.method == 'POST':
        empleado.nombre = request.form['nombre']
        empleado.ap_paterno = request.form['ap_paterno']
        empleado.ap_materno = request.form['ap_materno']
        empleado.departamento = request.form['departamento']
        empleado.puesto = request.form['puesto']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update_empleado.html', empleado=empleado)

#Ruta /empleados
@app.route('/empleados')
def getEmpleados():
    return 'Aqui van los empleados'

if __name__ == '__main__':
    app.run(debug=True)