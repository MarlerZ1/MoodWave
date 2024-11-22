class IncorrectDialoguePeopleNumber(Exception):
    """В диалоге должно быть ровно 2 человека"""


class UserToChatAccessError(Exception):
    """У пользователя нет доступа к этому чату"""