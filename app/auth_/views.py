import logging
import random
import string
from datetime import datetime

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user
from itsdangerous import BadSignature, BadTimeSignature, URLSafeTimedSerializer
from sqlalchemy import exc
from werkzeug.security import check_password_hash, generate_password_hash

from app.database import db
from app.email import send_email

from app.auth_.forms import AuthForm, RegisterForm
from app.auth_.models import User

auth_ = Blueprint('auth_', __name__, url_prefix='/auth')

logger = logging.getLogger(__name__)


@auth_.route('/login', methods=('GET', 'POST'))
def login():

    form_ = AuthForm(request.form)

    if request.method.__eq__('POST'):
        if form_.validate():
            email = request.form.get('email')
            password = request.form.get('password')

            try:
                user_ = User.query.filter_by(email=email.lower()).first()
            except (AttributeError, exc.DataError) as ex:
                logger.exception(ex)
                user_ = None

            if user_ is not None:
                if user_.confirmed.__ne__(True):
                    try:

                        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
                        token = serializer.dumps(user_.email, salt=current_app.config['MAIL_CONFIRM_SALT'])

                        link = request.url_root.rstrip('/') + url_for('.confirm_email', token=token)

                        send_email(
                            user_.email,
                            'Подтвердите почту на сервисе Fotty',
                            '/email/confirmed_email',
                            link=link
                        )

                        flash('Письмо отправлено!!!')

                        return redirect(url_for('.login'))

                    except Exception as ex:
                        logger.exception(ex)
                        flash('При отправки письма произошла ошибка!!!')

                elif check_password_hash(user_.password, password):
                    login_user(user=user_, remember=True)

                    return redirect(url_for('profile.index'))
                else:
                    flash('Не верный пароль!!!')
            else:
                flash('Пользователь не существует!!!')
        else:
            text_error = ''
            for error in form_.errors:
                text_error += f"{error}: {form_.errors[error][0]}<br>"
            flash(text_error)

    return render_template('login.html', title='Fotty - Login', form=form_)


@auth_.route('/registration', methods=('POST', 'GET'))
def registration():
    """Метод регистрации

    :return: страницу
    :rtype: flask.render_template
    """

    form_ = RegisterForm(request.form)

    if request.method.__eq__('POST'):
        if form_.validate():
            user_name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')
            phone = request.form.get('phone')

            # обработка телефона
            phone = phone.replace('(', '')
            phone = phone.replace(')', '')
            phone = phone.replace('+', '')
            phone = phone.replace('-', '')
            phone = phone.replace(' ', '')

            user = User()
            user.name = user_name.strip().lower()
            user.email = email.lower()
            user.password = generate_password_hash(password)

            user.created_at = datetime.now()
            user.updated_at = datetime.now()

            user.phone = phone
            user.confirmed = False

            db.session.add(user)
            db.session.commit()

            try:

                serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
                token = serializer.dumps(user.email, salt=current_app.config['MAIL_CONFIRM_SALT'])

                link = request.url_root.rstrip('/') + url_for('.confirm_email', token=token)

                send_email(
                    email,
                    'Подтвердите почту на сервисе Fotty',
                    '/email/confirmed_email',
                    link=link
                )

                flash('Письмо отправлено!!!')

                return redirect(url_for('.login'))

            except Exception as ex:
                logger.exception(ex)
                flash('При отправки письма произошла ошибка!!!')
        else:
            text_error = ''
            for error in form_.errors:
                text_error += f"{error}: {form_.errors[error][0]}<br>"
            flash(text_error)

    return render_template('registration.html', title='Fotty - Registration', form=form_)


@auth_.route('/forgot', methods=('GET', 'POST'))
def forgot_password():

    if request.method.__eq__('POST'):
        email = request.form.get('email')
        if email is not None:
            try:
                user_ = User.query.filter_by(email=email.lower()).first()
                if user_ is not None:
                    chars = string.ascii_letters + string.digits
                    passwd = ''.join(random.choice(chars) for i in range(12))

                    user_.password = generate_password_hash(passwd)
                    try:
                        send_email(
                            email,
                            'Новый пароль для сервиса Fotty',
                            '/email/forgot-passwd',
                            passwd=passwd
                        )

                        flash('Письмо отправлено!!!')

                        db.session.add(user_)
                        db.session.commit()

                        return redirect(url_for('.login'))

                    except Exception as ex:
                        logger.exception(ex)
                        flash('При отправки письма произршла ошибка!!!')
                else:
                    flash('Данного адреса не существует!!!')
            except (AttributeError, exc.DataError) as ex:
                logger.exception(ex)
                flash('Данного адреса не существует!!!')
        else:
            flash('Неккоректный email!!!')

    return render_template('forgot-password.html', title='Fotty - forgot')


@auth_.route('/confirm/email/<token>')
def confirm_email(token):
    """Для подтверждения email

    Parameters
    ----------
    token : string
        Токен доступа

    Returns
    -------
    Flask.redirect(index, login)
        Рендерит шаблон из папки шаблонов с заданным контекстом
    """

    try:

        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

        email = serializer.loads(
            token,
            salt=current_app.config['MAIL_CONFIRM_SALT'],
            max_age=3600
        )

        if email is not None:

            user_ = User.query.filter_by(email=email.lower()).first()

            if user_ is not None:
                user_.confirmed = True
                user_.updated_at = datetime.now()

                db.session.add(user_)
                db.session.commit()

                flash('Успешное подтверждение email!!!')

                login_user(user_, remember=True)

                return redirect(url_for('profile.index'))

            else:
                flash('Нет пользователя с таким email!!!')
                return redirect(url_for('.login'))

    except (BadTimeSignature, BadSignature, AttributeError, exc.DataError) as ex:
        # оповещение
        logger.exception(ex)
        return redirect(url_for('.login'))

    return redirect(url_for('.index'))


@auth_.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('.login'))
