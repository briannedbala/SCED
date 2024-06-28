from flask import Flask, render_template, redirect, request, flash, url_for
from flask_mysqldb import MySQL
from config import config

app = Flask(__name__)

db = MySQL(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Obtener datos del formulario
        username = request.form['username']
        password = request.form['password']

        cur = db.connection.cursor()
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cur.execute(query, (username, password))
        user = cur.fetchone()
        cur.close()

        try:
            # Vereficar en la base de datos
            if user:
                # Inicio de sesion exitoso
                flash('¡Inicio de sesion exitoso!', 'success')
                return redirect(url_for('shop'))
            else:
                # Inicio de sesion fallido
                flash('No puede ingresar, intente nuevamente', 'danger')
                return redirect(url_for('index'))
        except Exception as e:
            flash(str(e), 'danger')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Obtener datos del formulario
        fullname = request.form['fullname']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        neighborhood = request.form['neighborhood']

        try:
            # Insertar en la base de datos
            cur = db.connection.cursor()
            query = "INSERT INTO users (username, password, fullname, email, neighborhood) VALUES (%s, %s, %s, %s, %s)"
            cur.execute(query, (username, password,
                        fullname, email, neighborhood))
            db.connection.commit()
            cur.close()
            flash('¡Registro exitoso! Por favor, inicia sesión.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Error al registrar: {e}', 'danger')
            db.connection.rollback()

    return render_template('register.html')


@app.route('/options')
def options():
    return render_template('options.html')


@app.route('/register_patient', methods=['GET', 'POST'])
def registrar_paciente():
    if request.method == 'POST':
        fullname = request.form['fullname']
        age = request.form['age']
        dni = request.form['dni']
        gender = request.form['gender']
        neighborhood = request.form['neighborhood']
        street = request.form['street']
        grupo = request.form['grupo']
        print(fullname, age, dni, gender, neighborhood, street, grupo)

        try:
            cur = db.connection.cursor()
            query = "INSERT INTO patients (fullname, age, dni, gender, neighborhood, street, grupo) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cur.execute(query, (fullname, age, dni, gender,
                        neighborhood, street, grupo))
            db.connection.commit()
            cur.close()
            flash('Registro del paciente exitoso', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Error al registrar el paciente: {e}', 'danger')
            db.connection.rollback()

    return render_template('registrar_paciente.html')


@app.route('/view')
def view():
    try:
        cur = db.connection.cursor()
        query = "SELECT * FROM patients"
        cur.execute(query)
        patients = cur.fetchall()
        cur.close()
        return render_template('view.html', patients=patients)
    except Exception as e:
        flash(f'Error al obtener los datos', 'danger')
        return render_template('option')


@app.route('/search_patient', methods=['GET', 'POST'])
def search_patient():
    if request.form == 'POST':
        dni = request.form['dni']

        try:
            cur = db.connection.cursor()
            query = "SELECT * FROM patients WHERE dni = %s"
            cur.execute(query, [dni])
            patient = cur.fetchone()
            cur.close()

            if patient:
                return render_template('update_patient.html', patient=patient)
            else:
                flash('Paciente no encontrado', 'danger')
                return redirect(url_for(search_patient))
        except Exception as e:
            flash(f'Error al buscar el paciente: {e}', 'danger')
            return redirect(url_for('index'))

    return render_template('search_patient.html')


# @app.route('/update')
# def update():
#     try:
#         cur = db.connection.cursor()
#         query = "SELECT"
#     return render_template('update.html')


if __name__ == ('__main__'):
    app.config.from_object(config['development'])
    app.run()
