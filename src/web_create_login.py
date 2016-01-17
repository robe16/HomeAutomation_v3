from urllib import urlopen
from config_users import get_usernames

def html_users():
    return urlopen('web/login.html').read().encode('utf-8').format(users=_useritems())


def _useritems():
    data = get_usernames()
    STRhtml = ""
    STRhtml += '<div class="col-md-10 col-md-offset-1">'
    if data is None:
        STRhtml += '<p>No users are available on the server. Please continue as guest</p>'
        STRhtml += '<p>Users can be added within the settings pages</p>'
    else:
        STRhtml += '<form action="login">'
        x=0
        while x<len(data):
            username = data[x]
            STRhtml += urlopen('web/login_items.html').read().encode('utf-8').format(name=username)
            x += 1
        STRhtml += '<button class="btn btn-success btn-block" type="submit">Continue</button>'
        STRhtml += '</form>'
    STRhtml += '<button class="btn btn-default btn-block" onclick="window.location.href={guest}">Continue as guest</button>'.format(guest="'/web/login?user=Guest'")
    STRhtml += '</div>'
    return STRhtml