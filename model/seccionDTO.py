import sirope


class Seccion:
    def __init__(self, email, name):
        self.__email = email
        self.__name = name
        self.__notas = []

    @property
    def usr_email(self):
        return self.__email

    @property
    def name(self):
        return self.__name

    @property
    def notas(self):
        return self.__notas

    def get_safe_id(self, srp):
        return srp.safe_from_oid(self.__oid__)

    def add_nota(self, nota):
        if nota.section == self.name:
            self.__notas.append(nota)

    def remove_nota(self, title):
        for nota in self.__notas:
            if nota.title == title:
                self.__notas.remove(nota)
                return True
        return False

    def __str__(self):
        notas_str = "\n  ".join(str(nota) for nota in self.__notas)
        return f"Sección {self.name} (de {self.usr_email}):\n  {notas_str}"
