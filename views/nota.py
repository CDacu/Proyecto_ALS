import flask
import sirope
import flask_login

from model.seccionDTO import Seccion
from model.userDTO import User
from model.notaDTO import Nota


def get_blprint():
    nota_module = flask.blueprints.Blueprint("nota_blpr", __name__,
                                             url_prefix="/nota",
                                             template_folder="templates",
                                             static_folder="static")
    srp = sirope.Sirope()
    return nota_module, srp


nota_blpr, srp = get_blprint()


@flask_login.login_required
@nota_blpr.route("/add", methods=["GET", "POST"])
def nota_add():
    if flask.request.method == "GET":
        seccion_list = list(srp.filter(Seccion, lambda s: s.usr_email == User.current().email))
        data = {"usr": User.current(), "seccion_list": seccion_list}
        return flask.render_template("add_nota.html", **data)
    else:
        usr = User.current()
        nota_title = flask.request.form.get("edTitle", "").strip()
        nota_type = flask.request.form.get("edType", "").strip()
        nota_section = flask.request.form.get("edSection", "").strip()

        if nota_type == "normal":
            nota_content = flask.request.form.get("edContent", "").strip()
        elif nota_type == "lista":
            nota_content = flask.request.form.get("edLista", "").strip().split(',')
        elif nota_type == "enlace":
            nota_content = {
                "url": flask.request.form.get("edEnlace", "").strip(),
                "text": flask.request.form.get("edTexto", "").strip()
            }
        else:
            nota_content = ""

        if not nota_title:
            flask.flash("El título de la nota no puede estar vacío.")
            return flask.redirect("/nota/add")

        srp.save(Nota(usr.email, nota_title, nota_content, nota_type, nota_section))

        flask.flash("Nota añadida exitosamente.")
        return flask.redirect("/")


@flask_login.login_required
@nota_blpr.route("/delete")
def nota_delete():
    nota = Nota.find(srp, int(flask.request.args.get("nota_id", "").strip()))

    if nota:
        srp.delete(nota.__oid__)
        flask.flash("Nota borrada.")
    else:
        flask.flash("Nota no encontrada.")

    return flask.redirect("/")


@flask_login.login_required
@nota_blpr.route("/edit/<oid>", methods=["GET", "POST"])
def nota_edit(oid):
    usr = User.current()
    nota = Nota.find(srp, int(oid))

    if flask.request.method == "GET":
        if not nota or nota.usr_email != usr.email:
            flask.flash("Nota no encontrada o no autorizada.")
            return flask.redirect("/")

        seccion_list = list(srp.filter(Seccion, lambda s: s.usr_email == User.current().email))
        data = {"usr": usr, "nota": nota, "seccion_list": seccion_list}
        return flask.render_template("edit_nota.html", **data)
    else:
        nota_title = flask.request.form.get("edTitle", "").strip()
        nota_type = flask.request.form.get("edType", "").strip()
        nota_section = flask.request.form.get("edSection", "").strip()

        if nota_type == "normal":
            nota_content = flask.request.form.get("edContent", "").strip()
        elif nota_type == "lista":
            nota_content = flask.request.form.get("edLista", "").strip().split(',')
        elif nota_type == "enlace":
            nota_content = {
                "url": flask.request.form.get("edEnlace", "").strip(),
                "text": flask.request.form.get("edTexto", "").strip()
            }
        else:
            nota_content = ""

        if not nota_title:
            flask.flash("El título de la nota no puede estar vacío.")
            return flask.redirect(f"/nota/edit/{oid}")

        nota.title = nota_title
        nota.content = nota_content
        nota.note_type = nota_type
        nota.section = nota_section
        srp.save(nota)

        flask.flash("Nota actualizada exitosamente.")
        return flask.redirect("/")