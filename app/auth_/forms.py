from wtforms import form, validators, StringField, PasswordField, BooleanField, SubmitField


class RegisterForm(form.Form):
    """
    Форма регистрации
    """
    name = StringField('Name', validators=[validators.DataRequired(message='Обязательное поле для заполнения')])
    email = StringField('Email', validators=[validators.DataRequired(message='Обязательное поле для заполнения'),
                                             validators.Email(message='Неверный адрес электронной почты')])
    password = PasswordField('Пароль', validators=[
        validators.DataRequired(message='Обязательное поле для заполнения'),
        validators.Length(min=8, max=20, message='Поле должно быть длиной от 8 до 20 символов')])

    policy = BooleanField('Agree the terms and policy', validators=[
                          validators.DataRequired(message='Обязательное поле для заполнения')])

    submit = SubmitField("Submit")


class AuthForm(form.Form):
    """
    Форма авторизации
    """
    email = StringField('Email', validators=[validators.DataRequired(message='Обязательное поле для заполнения'),
                                             validators.Email(message='Неверный адрес электронной почты')])
    password = PasswordField('Пароль', validators=[
        validators.DataRequired(message='Обязательное поле для заполнения'),
        validators.Length(min=8, max=20, message='Поле должно быть длиной от 8 до 20 символов')])

    submit = SubmitField("Submit")
