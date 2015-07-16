from src.bottle import route, run

@route('/')
def hello():
    return "Hello World!"

run(host='localhost', port=8080, debug=True)

# to test, use the url below in the web browser
# http://localhost:8080/