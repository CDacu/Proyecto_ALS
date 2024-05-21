import flask
import sirope
import flask_login

from model.userDTO import User
from model.seccionDTO import Seccion


def get_blprint():
    seccion_module = flask.blueprints.Blueprint("seccion_blpr", __name__,
                                                url_prefix="/seccion",
                                                template_folder="templates/seccion",
                                                static_folder="static/seccion")
    srp = sirope.Sirope()
    return seccion_module, srp


seccion_blpr, srp = get_blprint()


@flask_login.login_required
@seccion_blpr.route("add", methods=["GET", "POST"])
def seccion_add():
    if flask.request.method == "GET":
        sust = {
            "usr": User.current()
        }
        return flask.render_template("add_seccion.html", **sust)
    else:
        usr = User.current()
        seccion_name = flask.request.form.get("edName", "").strip()

        if not seccion_name:
            flask.flash("Faltan datos de la sección.")
            return flask.redirect(flask.url_for("seccion_blpr.seccion_add"))

        srp.save(Seccion(usr.email, seccion_name))
        flask.flash(f"Sección '{seccion_name}' añadida.")
        return flask.redirect("/")


@flask_login.login_required
@seccion_blpr.route("/delete")
def seccion_delete():
    seccion_oid = flask.request.args.get("seccion_id", "").strip()
    seccion = srp.oid_from_safe(seccion_oid)

    if seccion:
        srp.delete(seccion)
        flask.flash("Sección borrada.")
    else:
        flask.flash("Sección no encontrada.")

    return flask.redirect("/")


@flask_login.login_required
@seccion_blpr.route("/edit", methods=["GET", "POST"])
def seccion_edit():
    if flask.request.method == "GET":
        seccion_oid = flask.request.args.get("seccion_id", "").strip()
        seccion = srp.oid_from_safe(seccion_oid)

        if seccion:
            sust = {
                "usr": User.current(),
                "seccion": seccion
            }
            return flask.render_template("edit_seccion.html", **sust)
        else:
            flask.flash("Sección no encontrada.")
            return flask.redirect("/")
    else:
        seccion_oid = flask.request.form.get("seccion_id", "").strip()
        seccion = srp.oid_from_safe(seccion_oid)

        if seccion:
            seccion.name = flask.request.form.get("edName", "").strip()
            srp.save(seccion)
            flask.flash(f"Sección '{seccion.name}' modificada.")
        else:
            flask.flash("Sección no encontrada.")

        return flask.redirect("/")
