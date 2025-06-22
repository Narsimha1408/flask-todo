from flask import Flask, render_template

app=Flask(__name__)

@app.route("/products")
def products():
    return "this is products page"


@app.route("/")
def test():
    return "<h1>Hi darling</h1>"

@app.route("/rendering-page")
def renderPage():
    return render_template("index.html")

if __name__== "__main__":
    app.run(debug=True, port = 5000)