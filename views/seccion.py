import flask
import sirope
import flask_login

from model.userDTO import User
from model.seccionDTO import Seccion


def get_blprint():
    seccion_module = flask.blueprints.Blueprint("seccion_blpr", __name__,
                                                url_prefix="/seccion",
                                                template_folder="templates",
                                                static_folder="static")
    srp = sirope.Sirope()
    return seccion_module, srp


seccion_blpr, srp = get_blprint()


@flask_login.login_required
@seccion_blpr.route("/add", methods=["GET", "POST"])
def seccion_add():
    if flask.request.method == "GET":
        data = {"usr": User.current()}
        return flask.render_template("add_seccion.html", **data)
    else:
        usr = User.current()
        seccion_name = flask.request.form.get("edName", "").strip()

        if not seccion_name:
            flask.flash("El nombre de la sección no puede estar vacío.")
            return flask.redirect("/seccion/add")

        # Verificar si ya existe una sección con el mismo nombre para el usuario
        existing_seccion = srp.find_first(Seccion, lambda s: s.name == seccion_name and s.usr_email == usr.email)
        if existing_seccion:
            flask.flash("Ya existe una sección con este nombre.")
            return flask.redirect("/seccion/add")

        new_seccion = Seccion(usr.email, seccion_name)
        srp.save(new_seccion)

        flask.flash("Sección añadida exitosamente.")
        return flask.redirect("/")


@flask_login.login_required
@seccion_blpr.route("/delete")
def seccion_delete():
    seccion = Seccion.find(srp, int(flask.request.args.get("seccion_id", "").strip()))

    if seccion:
        srp.delete(seccion.__oid__)
        flask.flash("Sección borrada.")
    else:
        flask.flash("Sección no encontrada.")

    return flask.redirect("/")


@flask_login.login_required
@seccion_blpr.route("/edit/<oid>", methods=["GET", "POST"])
def seccion_edit(oid):
    usr = User.current()
    seccion = Seccion.find(srp, int(oid))

    if flask.request.method == "GET":
        if not seccion or seccion.usr_email != usr.email:
            flask.flash("Sección no encontrada o no autorizada.")
            return flask.redirect("/")

        data = {"usr": usr, "seccion": seccion}
        return flask.render_template("edit_seccion.html", **data)
    else:
        seccion_name = flask.request.form.get("edName", "").strip()

        if not seccion_name:
            flask.flash("El nombre de la sección no puede estar vacío.")
            return flask.redirect(f"/seccion/edit/{oid}")

        # Verificar si ya existe una sección con el mismo nombre para el usuario, excluyendo la sección actual
        existing_seccion = srp.find_first(Seccion, lambda s: s.name == seccion_name and
                                                             s.usr_email == usr.email and
                                                             s.oid != oid)
        if existing_seccion:
            flask.flash("Ya existe una sección con este nombre.")
            return flask.redirect(f"/seccion/edit/{oid}")

        seccion.name = seccion_name
        srp.save(seccion)

        flask.flash("Sección actualizada exitosamente.")
        return flask.redirect("/")
