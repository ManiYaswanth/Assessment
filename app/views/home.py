from flask import Blueprint, render_template

mod = Blueprint("home", __name__, template_folder="templates")

@mod.route('/home', methods=['GET'])
def render_home():
    return render_template("home.html")
