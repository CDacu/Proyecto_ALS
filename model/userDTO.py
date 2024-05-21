import sirope
import flask_login
import werkzeug.security as safe


class User(flask_login.mixins.UserMixin):
    def __init__(self, email, pswd):
        self.__email = email
        self.__pswd = safe.generate_password_hash(pswd)

    @property
    def email(self):
        return self.__email

    def get_id(self):
        return self.email

    def chk_pswd(self, other_pswd):
        return safe.check_password_hash(self.__pswd, other_pswd)

    @staticmethod
    def current():
        usr = flask_login.current_user

        if usr.is_anonymous:
            flask_login.logout_user()
            usr = None

        return usr

    @staticmethod
    def find(srp: sirope.Sirope, email: str) -> "User":
        return srp.find_first(User, lambda u: u.email == email)
