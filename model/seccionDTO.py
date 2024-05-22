import sirope


class Seccion:
    def __init__(self, email, name):
        self.__email = email
        self.__name = name

    @property
    def usr_email(self):
        return self.__email

    @property
    def oid(self):
        return self.__oid__.num

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    def get_safe_id(self, srp):
        return srp.safe_from_oid(self.__oid__)

    @staticmethod
    def find(srp: sirope.Sirope, oid: int) -> "Seccion":
        return srp.find_first(Seccion, lambda s: s.oid == oid)

    def __str__(self):
        notas_str = "\n  ".join(str(nota) for nota in self.__notas)
        return f"Sección {self.name} (de {self.usr_email}):\n  {notas_str}"
