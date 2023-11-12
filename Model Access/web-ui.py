from flask import Flask, render_template

web_ui = Flask(__name__, template_folder="templates", static_folder="Assets")


@web_ui.route("/")
def main():
    return render_template("synthx.html")


if __name__ == "__main__":
    web_ui.run(debug=True)
