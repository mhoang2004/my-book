from flask import Flask, render_template, request

app = Flask(__name__)

COMPANY_NAME = "MyBooks"


@app.route("/")
def home():
    return render_template('home.html', style='home', company_name=COMPANY_NAME)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, use_debugger=False, use_reloader=False)
