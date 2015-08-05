from urllib import urlopen

def create_index():
    return urlopen('web/header.html').read().encode('utf-8')+urlopen('web/index.html').read().encode('utf-8')+urlopen('web/footer.html').read().encode('utf-8')

def create_loungetv():
    return urlopen('web/header.html').read().encode('utf-8')+urlopen('web/loungetv.html').read().encode('utf-8')+urlopen('web/footer.html').read().encode('utf-8')