import secrets
from abc import ABC, abstractmethod

COUNT_SYMBOL: int = 16


class AbstractTokenHelper(ABC):

    @abstractmethod
    def token_exists(self, token: str) -> bool:
        """
        Check if a token is exists
        :param token:
        :return:
        """

    @abstractmethod
    def add_token(self, token: str) -> None:
        """
        Save token in storage
        :param token:
        :return:
        """

    @abstractmethod
    def get_tokens(self) -> list[str]:
        """
        All tokens
        :return:
        """

    @classmethod
    def generate_token(cls) -> str:
        return secrets.token_urlsafe(COUNT_SYMBOL)

    def generate_and_save_token(self) -> str:
        token = self.generate_token()
        self.add_token(token)
        return token
