import json
import flask
import flask_login
import sirope

from model.userDTO import User
from model.notaDTO import Nota
from model.seccionDTO import Seccion

from views.user import user_blpr
from views.nota import nota_blpr
from views.seccion import seccion_blpr


def create_app():
    flapp = flask.Flask(__name__)
    sirop = sirope.Sirope()
    login = flask_login.LoginManager()

    flapp.config.from_file("instance/config.json", json.load)
    login.init_app(flapp)
    flapp.register_blueprint(user_blpr)
    flapp.register_blueprint(nota_blpr)
    flapp.register_blueprint(seccion_blpr)

    @login.unauthorized_handler
    def unauthorized_handler():
        flask.flash("Unauthorized access.")
        return flask.redirect("/")

    @login.user_loader
    def user_loader(email: str) -> User:
        return User.find(sirop, email)

    return flapp, sirop, login


app, srp, lm = create_app()


@app.route("/favicon.ico")
def get_fav_icon():
    return app.send_static_file("favicon.ico")


@app.route("/login", methods=["POST"])
def login():
    if User.current():
        flask_login.logout_user()
        flask.flash("Ha pasado algo extraño. Por favor, entra de nuevo.")
        return flask.redirect("/")

    usr_email = flask.request.form.get("edEmail", "").strip()
    usr_pswd = flask.request.form.get("edPswd", "").strip()

    if not usr_email or not usr_pswd:
        flask.flash("Credenciales incompletas")
        return flask.redirect("/")

    usr = User.find(srp, usr_email)

    if not usr or not usr.chk_pswd(usr_pswd):
        flask.flash("Credenciales incorrectas: ¿has hecho el registro?")
        return flask.redirect("/")

    flask_login.login_user(usr)
    return flask.redirect("/")


@flask_login.login_required
@app.route("/logout")
def logout():
    flask_login.logout_user()
    return flask.redirect("/")


@app.route("/")
def main():
    usr = User.current()
    nota_list = []
    seccion_list = []
    notas_por_seccion = {}
    notas_sin_seccion = []

    if usr:
        nota_list = list(srp.filter(Nota, lambda n: n.usr_email == usr.email))
        seccion_list = list(srp.filter(Seccion, lambda s: s.usr_email == usr.email))

        for seccion in seccion_list:
            notas_por_seccion[seccion] = [nota for nota in nota_list if nota.section == seccion.name]

        notas_sin_seccion = [nota for nota in nota_list if not nota.section]

    sust = {
        "usr": usr,
        "srp": srp,
        "nota_list": nota_list,
        "seccion_list": seccion_list,
        "notas_por_seccion": notas_por_seccion,
        "notas_sin_seccion": notas_sin_seccion
    }

    return flask.render_template("index.html", **sust)


if __name__ == "__main__":
    app.run(debug=True)
