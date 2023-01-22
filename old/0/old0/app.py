from flask import Flask, render_template, request

app = Flask(__name__) # __name__ refers to the same file. It turns the file to a flask application


@app.route("/")
def index():
    name = request.args.get("name", "World")
    return render_template("index.html", name=name)
