from urllib import urlopen

def create_index():
    return urlopen('web_templates/header.html').read()+urlopen('web_templates/index.html').read()+urlopen('web_templates/footer.html').read()