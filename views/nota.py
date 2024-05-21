import flask
import sirope
import flask_login

from model.userDTO import User
from model.notaDTO import Nota


def get_blprint():
    nota_module = flask.blueprints.Blueprint("nota_blpr", __name__,
                                             url_prefix="/nota",
                                             template_folder="templates/nota",
                                             static_folder="static/nota")
    srp = sirope.Sirope()
    return nota_module, srp


nota_blpr, srp = get_blprint()


@flask_login.login_required
@nota_blpr.route("add", methods=["GET", "POST"])
def nota_add():
    if flask.request.method == "GET":
        sust = {
            "usr": User.current()
        }
        return flask.render_template("add_nota.html", **sust)
    else:
        usr = User.current()
        nota_title = flask.request.form.get("edTitle", "").strip()
        nota_content = flask.request.form.get("edContent", "").strip()
        nota_type = flask.request.form.get("edType", "").strip()
        nota_section = flask.request.form.get("edSection", "").strip()

        if not nota_title or not nota_content or not nota_type:
            flask.flash("Faltan datos de la nota.")
            return flask.redirect(flask.url_for("nota_blpr.nota_add"))

        srp.save(Nota(usr.email, nota_title, nota_content, nota_type, nota_section))
        flask.flash(f"Nota '{nota_title}' añadida.")
        return flask.redirect("/")


@flask_login.login_required
@nota_blpr.route("/delete")
def nota_delete():
    nota_oid = flask.request.args.get("nota_id", "").strip()
    nota = srp.oid_from_safe(nota_oid)

    if nota:
        srp.delete(nota)
        flask.flash("Nota borrada.")
    else:
        flask.flash("Nota no encontrada.")

    return flask.redirect("/")


@flask_login.login_required
@nota_blpr.route("/edit", methods=["GET", "POST"])
def nota_edit():
    if flask.request.method == "GET":
        nota_oid = flask.request.args.get("nota_id", "").strip()
        nota = srp.oid_from_safe(nota_oid)

        if nota:
            sust = {
                "usr": User.current(),
                "nota": nota
            }
            return flask.render_template("edit_nota.html", **sust)
        else:
            flask.flash("Nota no encontrada.")
            return flask.redirect("/")
    else:
        nota_oid = flask.request.form.get("nota_id", "").strip()
        nota = srp.oid_from_safe(nota_oid)

        if nota:
            nota.title = flask.request.form.get("edTitle", "").strip()
            nota.content = flask.request.form.get("edContent", "").strip()
            nota.note_type = flask.request.form.get("edType", "").strip()
            nota.section = flask.request.form.get("edSection", "").strip()
            srp.save(nota)
            flask.flash(f"Nota '{nota.title}' modificada.")
        else:
            flask.flash("Nota no encontrada.")

        return flask.redirect("/")
