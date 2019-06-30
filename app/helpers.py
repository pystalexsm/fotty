
def clear_phone(phone):
    """Очистка номера телефона от доп символов

    :param phone: номер телефона
    :type phone: string
    :return: номер телефона
    :rtype: string
    """

    phone = phone.replace('(', '')
    phone = phone.replace(')', '')
    phone = phone.replace('+', '')
    phone = phone.replace('-', '')
    phone = phone.replace(' ', '')

    return phone
