from flask import Flask # classes are capitalized, packages are not.

app = Flask(__name__) # "__name__" gives each file a unique name

@app.route("/") # "http://www.google.com/"
def index():
    return "Hello world!"

app.run(port=6000)