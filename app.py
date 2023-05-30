from flask import Flask, render_template_string
from template import parse_template

app = Flask(__name__)

context = {
    "user_name": "Student A",
    "user_age": 23,
    "user_department": "IST",
    "is_undergraduate": False,
}


@app.route("/")
def homepage():
    return render_template_string(parse_template("index.html", context=context))
