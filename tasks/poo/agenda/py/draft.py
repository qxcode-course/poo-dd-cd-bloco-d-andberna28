class Fone:
    def __init__(self, id: str, number: str):
        self.__id = id
        self.__number = number

    def getId(self):
        return self.__id
    def getNumber(self):
        return self.__number

    def isValid(self):
        validos = "123456789()-"
        for c in self.__number:
            if c not in validos:
                return False
        return True
    
    def __str__(self):
        return f"{self.__id}:{self.__number}"

class Contact:
    def __init__(self, name):
        self.__name = name
        self.favorited = False
        self.__fones = []

    def getFones(self):
        return self.__fones
    def getName(self):
        return self.__name
    def setName(self, value):
        self.__name = value

    def addPhone(self, id: str, number: str):
        try:
            fone = Fone(id, number)
            if fone.isValid():
                self.__fones.append(fone)
                return
            print("fail: fone invalido")
        except Exception:
            print("fail: erro ao adicionar fone")

    def rmFone(self, index: int):
        try:
            if 0 <= index < len(self.__fones):
                self.__fones.pop(index)
                return
            print("fail: indice invalido")
        except Exception:
            print("fail: erro ao remover fone")

    def toggleFavorite(self):
        self.favorited = not self.favorited

    def isFavorited(self):
        return self.favorited
    
    def __str__(self):
        prefixo = "@" if self.favorited else "-"
        fones_str = ", ".join([f"{fone}" for fone in self.__fones])
        return f"{prefixo} {self.__name} [{fones_str}]"

class Agenda:
    def __init__(self):
        self.contacts = []

    def findPosByName(self, name):
        for i, c in enumerate(self.contacts):
            if c.getName() == name:
                return i
        return -1

    def addContact(self, name, fones):
        try:
            pos = self.findPosByName(name)
            if pos != -1:
                contact = self.contacts[pos]
                for f in fones:
                    contact.addPhone(f.getId(), f.getNumber())
            else:
                contact = Contact(name)
                for f in fones:
                    contact.addPhone(f.getId(), f.getNumber())
                self.contacts.append(contact)
                self.contacts.sort(key=lambda c: c.getName())
        except Exception:
            print("fail: erro ao adicionar contato")

    def getContact(self, name):
        pos = self.findPosByName(name)
        if pos != -1:
            return self.contacts[pos]
        return None

    def rmContact(self, name):
        try:
            pos = self.findPosByName(name)
            if pos != -1:
                self.contacts.pop(pos)
                return
            print("fail: contato nao existe")
        except Exception:
            print("fail: erro ao remover contato")

    def search(self, pattern):
        try:
            resultado = []
            for c in self.contacts:
                s = str(c)
                if pattern in s:
                    resultado.append(c)
            return resultado
        except Exception:
            print("fail: erro na busca")
            return []

    def getFavorited(self):
        return [c for c in self.contacts if c.isFavorited()]

    def __str__(self):
        return "\n".join(str(c) for c in self.contacts)

def main():
    agenda = Agenda()
    while True:
        try:
            line: str = input()
            print("$" + line)
            args: list[str] = line.split(" ")
            if args[0] == "end":
                break

            elif args[0] == "show":
                print(agenda)
                
            elif args[0] == "add":
                try:
                    fones = []
                    for token in args[2:]:
                        try:
                            id, num = token.split(":")
                            fones.append(Fone(id, num))
                        except ValueError:
                            print("fail: formato do fone invalido")
                    agenda.addContact(args[1], fones)
                except Exception:
                    print("fail: erro no comando add")

            elif args[0] == "rmFone":
                try:
                    contato = agenda.getContact(args[1])
                    if contato:
                        contato.rmFone(int(args[2]))
                    else:
                        print("fail: contato nao encontrado")
                except ValueError:
                    print("fail: indice invalido")
                except Exception:
                    print("fail: erro ao remover fone")

            elif args[0] == "rm":
                try:
                    agenda.rmContact(args[1])
                except Exception:
                    print("fail: erro no comando rm")

            elif args[0] == "search":
                try: 
                    for c in agenda.search(args[1]):
                        print(c)
                except Exception:
                    print("fail: erro no search")

            elif args[0] == "tfav":
                try:
                    contato = agenda.getContact(args[1])
                    if contato:
                        contato.toggleFavorite()
                    else:
                        print("fail: contato nao encontrado")
                except Exception:
                    print("fail: erro no comando tfav")

            elif args[0] == "favs":
                for c in agenda.getFavorited():
                    print(c)

            else:
                print("fail: comando invalido")

        except EOFError:
            break
        except KeyboardInterrupt:
            print("\nEncerrado pelo usuário.")
            break
        except Exception as e:
            print("fail: erro inesperado:", e)

    
main()