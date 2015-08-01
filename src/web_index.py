from urllib import urlopen

def create_index():
    return urlopen('web/header.html').read()+urlopen('web/index.html').read()+urlopen('web/footer.html').read()