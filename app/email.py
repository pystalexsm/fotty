from flask import current_app, render_template
from flask_mail import Mail, Message
from threading import Thread

mail = Mail()


def _send_async_email(_app, msg):
    """
    Для асинхронной отправки писем
    :param _app: приложение контекст
    :param msg: сообщение
    :return: void
    """
    with _app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    """
    Отпрака email
    :param to: кому
    :param subject: тема
    :param template: шаблон
    :param kwargs: парасктры
    :return: Thread
    """

    app = current_app._get_current_object()

    msg = Message(
        subject=subject,
        recipients=[to],
        html=render_template(template + '.html', **kwargs),
        # body=render_template(template + '.txt', **kwargs),
        sender=app.config['MAIL_DEFAULT_SENDER']
    )

    thr = Thread(target=_send_async_email, args=(app, msg))
    thr.start()

    return thr
