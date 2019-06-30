from wtforms import form, validators, StringField, PasswordField, SubmitField


class RegisterForm(form.Form):
    """
    Форма регистрации
    """
    name = StringField(
        'Name', validators=[validators.DataRequired(message='Обязательное поле для заполнения')],
        render_kw={'class': 'form-control custom-input-form'})
    email = StringField(
        'Email',
        validators=[validators.DataRequired(message='Обязательное поле для заполнения'),
                    validators.Email(message='Неверный адрес электронной почты')],
        render_kw={'class': 'form-control custom-input-form'})
    phone = StringField(
        'Phone', validators=[validators.DataRequired(message='Обязательное поле для заполнения')],
        render_kw={'class': 'form-control custom-input-form'})
    password = PasswordField(
        'Пароль',
        validators=[validators.DataRequired(message='Обязательное поле для заполнения'),
                    validators.EqualTo('repassword', message='Пароли не совпадают'),
                    validators.Length(min=8, max=20, message='Поле должно быть длиной от 8 до 20 символов')],
        render_kw={'class': 'form-control custom-input-form'})

    repassword = PasswordField(
        'Пароль',
        validators=[validators.DataRequired(message='Обязательное поле для заполнения'),
                    validators.Length(min=8, max=20, message='Поле должно быть длиной от 8 до 20 символов')],
        render_kw={'class': 'form-control custom-input-form'})

    submit = SubmitField("Зарегистрироваться", render_kw={"class": "btn btn-primary btn-color-fotty btn-radius-fotty col-8"})

    def validate_phone(self, phone):

        phone = phone.data

        phone = phone.replace('(', '')
        phone = phone.replace(')', '')
        phone = phone.replace('+', '')
        phone = phone.replace('-', '')
        phone = phone.replace(' ', '')

        cnt = len(phone)
        # лучше использовать либу, но позже
        if cnt < 11 or cnt > 11:
            raise validators.ValidationError('Не верный формат телефона')


class AuthForm(form.Form):
    """
    Форма авторизации
    """
    email = StringField(
        'Электронный адрес',
        validators=[validators.DataRequired(message='Обязательное поле для заполнения'),
                    validators.Email(message='Неверный адрес электронной почты')],
        render_kw={'class': 'form-control custom-input-form'})
    password = PasswordField(
        'Пароль',
        validators=[validators.DataRequired(message='Обязательное поле для заполнения'),
                    validators.Length(min=8, max=20, message='Поле должно быть длиной от 8 до 20 символов')],
        render_kw={'class': 'form-control custom-input-form'})

    submit = SubmitField("Войти", render_kw={"class": "btn btn-primary btn-color-fotty btn-radius-fotty col-8"})
