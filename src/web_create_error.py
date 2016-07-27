from urllib import urlopen
from web_menu import html_menu


def create_error(user, code):
    if code == 404:
        body = urlopen('web/error.html').read().encode('utf-8').format(code='404',
                                                                       desc='Page not found',
                                                                       mesg='The page you are looking for does not exist!!')
    elif code == 500:
        body = urlopen('web/error.html').read().encode('utf-8').format(code='500',
                                                                       desc='Network error',
                                                                       mesg='There was an error with the code on the server!!')
    else:
        body = urlopen('web/error.html').read().encode('utf-8').format(code='---',
                                                                       desc='Unknown',
                                                                       mesg='An error has been encountered, please try again!!')
    #
    return urlopen('web/header.html').read().encode('utf-8').format(title=str(code)) + \
           html_menu(user) +\
           urlopen('web/body.html').read().encode('utf-8').format(header='', body=body) +\
           urlopen('web/footer.html').read().encode('utf-8')