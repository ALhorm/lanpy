from typing import Any
from ..lexer import Token
from ..errors import ParserError


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self._tokens = tokens
        self._pos = 0
        self.expressions = []
        self.statements = []

    def parse(self) -> None:
        """
        Executes statements until encounters an EOF token.

        :return: None
        """

        while not self.match('EOF'):
            self.exec_statement()

    def expression(self, function) -> None:
        """
        Decorator that adds a function to the list of expressions.

        :param function: function to be added (must return Expression or None).
        :return: None
        """

        self.expressions.append(function)

    def statement(self, function) -> None:
        """
        Decorator that adds a function to the list of statements.

        :param function: function to be added (must return Statement or None).
        :return: None
        """

        self.statements.append(function)

    def get_token(self, rel_pos: int) -> Token:
        """
        Adds the position passed in the parameter to the current position and returns a token for the resulting position.

        :param rel_pos: the relative position that will be added to the current position.
        :return: Token
        """

        position = self._pos + rel_pos
        if position >= len(self._tokens):
            return Token('EOF', '\0')
        return self._tokens[position]

    def match(self, token_name: str) -> bool:
        """
        Compares the name of the current token with the name passed to the function parameter. If the names match, increments the position by 1 and returns True, otherwise returns False.

        :param token_name: name of the expected token.
        :return: bool
        """

        current = self.get_token(0)
        if current.name != token_name:
            return False
        self._pos += 1
        return True

    def look_match(self, token_name: str, rel_pos: int) -> bool:
        """
        Adds the current position and the one passed as an argument and compares the name of the token obtained by the resulting position with the name passed to the function parameter.

        :param token_name: name of the expected token.
        :param rel_pos: the relative position that will be added to the current position.
        :return: bool
        """

        return self.get_token(rel_pos).name == token_name

    def consume(self, token_name: str) -> Token:
        """
        Compares the name of the current token with the name passed to the function parameter. If the names match, increments the position by 1 and returns current token, otherwise generates ParserError.

        :param token_name: name of the expected token.
        :return: Token
        """

        current = self.get_token(0)
        if current.name != token_name:
            raise ParserError(f'unexpected token: {current}.')
        self._pos += 1
        return current

    def get_expression(self) -> Any:
        """
        Goes through all expressions and returns the one that is not None.

        :return: Any
        """

        for expr in self.expressions:
            res = expr()
            if res is not None:
                return res.eval()

    def exec_statement(self) -> None:
        """
        Goes through all statements and executes the one that does not equal None.

        :return: None
        """

        for statement in self.statements:
            res = statement()
            if res is not None:
                res.exec()
