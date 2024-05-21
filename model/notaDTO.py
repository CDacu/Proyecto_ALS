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
    def title(self):
        return self.__title

    @property
    def content(self):
        return self.__content

    @property
    def note_type(self):
        return self.__note_type

    @property
    def section(self):
        return self.__section

    def get_safe_id(self, srp):
        return srp.safe_from_oid(self.__oid__)

    def __str__(self):
        return f"{self.title} ({self.note_type}): '{self.content}'"
