from flask import Flask, render_template
from api import routes
from views import home

app = Flask(__name__)

app.register_blueprint(routes.mod, url_prefix="/api/v1")
app.register_blueprint(home.mod, url_prefix="/")

@app.route("/")
def landing_page():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
