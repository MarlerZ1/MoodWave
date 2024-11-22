class IncorrectDialoguePeopleNumber(Exception):
    def __str__(self):
        return """В диалоге должно быть ровно 2 человека"""


class UserToChatAccessError(Exception):
    def __str__(self):
        return """У пользователя нет доступа к этому чату"""

