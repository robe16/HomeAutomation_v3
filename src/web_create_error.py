from urllib import urlopen
from web_menu import html_menu


def create_error_404(user, arr_devices):
    body = urlopen('web/error.html').read().encode('utf-8').format(code='400',
                                                                   desc='Page not found',
                                                                   mesg='The page you are looking for does not exist!!')
    return urlopen('web/header.html').read().encode('utf-8').format(title='400') + \
           html_menu(user, arr_devices) +\
           urlopen('web/body.html').read().encode('utf-8').format(body = body) +\
           urlopen('web/footer.html').read().encode('utf-8')


def create_error_500(user, arr_devices):
    body = urlopen('web/error.html').read().encode('utf-8').format(code='500',
                                                                   desc='Network error',
                                                                   mesg='There was an error with the code on the server!!')
    return urlopen('web/header.html').read().encode('utf-8').format(title='500') + \
           html_menu(user, arr_devices) +\
           urlopen('web/body.html').read().encode('utf-8').format(body = body) +\
           urlopen('web/footer.html').read().encode('utf-8')