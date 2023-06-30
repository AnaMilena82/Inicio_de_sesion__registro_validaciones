from flask import Flask, render_template, request, redirect, session, url_for, flash
from app_registerandlogin import app
from app_registerandlogin.models.model_users import User

@app.route('/', methods = ['GET'])    
@app.route('/register', methods = ['GET'])    
@app.route('/login', methods = ['GET'])    
def index():
    return render_template("index.html")



@app.route('/register', methods = ['POST'])    
def post_register():
    language = request.form.getlist('language')
    country_nac = request.form.get("country_nac")
    if not language:  # Si no se selecciona ningún idioma, establecer language como una lista vacía
        language = []
    data_register = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": request.form["password"],
        "confirmpassword": request.form["confirmpassword"],
        "fech_nac": request.form["fech_nac"],
        "country_nac": country_nac,
        "language" : language
        
    }

    if not User.validate_register(data_register):
        return redirect('/')
    
    user = User.new_user(data_register)
    session['user_id'] = user.id
    return redirect(url_for('success'))

@app.route('/login', methods = ['POST'])    
def post_login():
   
    data_login = {
        "email": request.form["email"],
        "password": request.form["password"],
    }
    if not User.validate_login(data_login):
       return redirect('/')
    
    user = User.get_user_by_email(data_login["email"])
    print("ESTA ES EL RESULTADO DE LA CONSULTA")
    print(user)
    if user:
        user_id = user.id
        session['user_id'] = user_id
        return redirect(url_for('success'))


@app.route('/success')
def success():
    user_id = session.get('user_id')
    if user_id:
        user = User.get_user_by_id(user_id)
        if user:
            return render_template('success.html', name=user.first_name)
    return redirect('/')            

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')     