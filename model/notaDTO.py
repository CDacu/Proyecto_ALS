import sirope


class Nota:
    def __init__(self, email, title, content, note_type, section=None):
        self.__email = email
        self.__title = title
        self.__content = content
        self.__note_type = note_type
        self.__section = section

    @property
    def usr_email(self):
        return self.__email

    @property
    def oid(self):
        return self.__oid__.num

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, title):
        self.__title = title

    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, content):
        self.__content = content

    @property
    def note_type(self):
        return self.__note_type

    @note_type.setter
    def note_type(self, note_type):
        self.__note_type = note_type

    @property
    def section(self):
        return self.__section

    @section.setter
    def section(self, section):
        self.__section = section

    def get_safe_id(self, srp):
        return srp.safe_from_oid(self.__oid__)

    def __str__(self):
        return f"{self.title} ({self.note_type}): '{self.content}'"

    @staticmethod
    def find(srp: sirope.Sirope, oid: int) -> "Nota":
        return srp.find_first(Nota, lambda n: n.oid == oid)
