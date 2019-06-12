from flask import flash, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash

from . import profile
from app.auth_.models import User
from app.database import db


@profile.route('/')
@login_required
def index():
    return render_template('profile.html', user=current_user, profile=True, title='Профиль')


@profile.route('/profile/edit/<int:id>', methods=('GET', 'POST'))
@login_required
def edit(id):

    if request.method.__eq__('POST'):
        name = request.form.get('name')
        phone = request.form.get('phone')
        passwd = request.form.get('password')
        repasswd = request.form.get('repassword')

        # обработка телефона
        phone = phone.replace('(', '')
        phone = phone.replace(')', '')
        phone = phone.replace('+', '')
        phone = phone.replace('-', '')
        phone = phone.replace(' ', '')

        if name and phone:
            user_ = User.query.filter_by(id=id).first()
            if user_ is not None:

                user_.name = name.strip().lower()
                user_.phone = phone

                if passwd is not None and len(passwd) > 0:
                    if passwd.__eq__(repasswd):
                        cnt_passwd = len(passwd)
                        if cnt_passwd >= 8 and cnt_passwd < 20:
                            user_.password = generate_password_hash(passwd)
                        else:
                            flash('Пароль не сохранен!!! Пароль должен быть от 8 до 20 символов')
                    else:
                        flash('Пароль не сохранен!!! Пароли не совпадают')

                db.session.add(user_)
                db.session.commit()

                flash('Данные успешно отредактированы!')

                return redirect(url_for('.edit', id=id))

        else:
            flash('Данные не прошли валидацию')

    return render_template('profile-edit.html', user=current_user, profile=True, title=f'Редауьтрование профиля № {id}')
