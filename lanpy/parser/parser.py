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
        while not self.match('EOF'):
            self.exec_statement()

    def expression(self, function) -> None:
        self.expressions.append(function)

    def statement(self, function) -> None:
        self.statements.append(function)

    def get_token(self, rel_pos: int) -> Token:
        position = self._pos + rel_pos
        if position >= len(self._tokens):
            return Token('EOF', '\0')
        return self._tokens[position]

    def match(self, token_name: str) -> bool:
        current = self.get_token(0)
        if current.name != token_name:
            return False
        self._pos += 1
        return True

    def look_match(self, token_name: str, rel_pos: int) -> bool:
        return self.get_token(rel_pos).name == token_name

    def consume(self, token_name: str) -> Token:
        current = self.get_token(0)
        if current.name != token_name:
            raise ParserError(f'unexpected token: {current}.')
        self._pos += 1
        return current

    def get_expression(self) -> Any:
        for expr in self.expressions:
            res = expr()
            if res is not None:
                return res.eval()

    def exec_statement(self) -> Any:
        for statement in self.statements:
            res = statement()
            if res is not None:
                res.exec()
