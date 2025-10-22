from abc import ABC, abstractmethod


class AbstractUserHelper(ABC):
    """
    Что нужно для обертки
     - получение пароля по юзернейму
     - Совпадает ли пароль с переданными
    """

    @abstractmethod
    def get_user_password(self, username: str) -> str | None:
        """
        По переданному юзернейму находит пароль

        Возвращает пароль, если есть.
        :param username - имя пользователя
        :return: - пароль по пользователю, если найден
        """

    @classmethod
    def check_password_match(cls, password1: str, password2: str) -> bool:
        """Проверка пароля на совпадения."""
        return password1 == password2

    def validate_user_password(self, username: str, password: str) -> bool:
        """
        Проверить валиден ли пароль

        :param username - чей пароль проверять
        :param password - переданный пароль. Сверить с тем, что в бд
        :return True если совпало, иначе False
        """

        db_password = self.get_user_password(username=username)

        if db_password is None:
            return False

        return self.check_password_match(
            password1=db_password,
            password2=password,
        )
