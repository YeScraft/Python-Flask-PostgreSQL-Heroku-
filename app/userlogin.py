# Необходим для работы LoginManager, описывает состояние текущего пользователя
class UserLogin:
    # Создаём экземпляр текущего пользователя передавая объект юзера из БД
    def __init__(self, user):
        self.__user = user

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    # Возвращиет id текущего пользователя
    def get_id(self):
        return str(self.__user.id)

    # Возвращиет имя текущего пользователя
    def get_name(self):
        return str(self.__user.username)
