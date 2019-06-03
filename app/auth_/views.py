from . import auth_
from flask import render_template


@auth_.route('/login')
def login():
    return render_template('login.html')


@auth_.route('/registration')
def registration():
    return render_template('register.html')
