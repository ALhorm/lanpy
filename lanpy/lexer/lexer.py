from .token import Token
from ..errors import LexerError


class Lexer:
    def __init__(self,
                 code: str,
                 operators: dict[str, str] = ...,
                 keywords: dict[str, str] = ...) -> None:
        self._code = code
        self._operators = operators
        self._keywords = keywords

        self._pos = 0
        self._tokens = []
        self._chars = ''

        if self._operators is not ...:
            for i in self._operators.keys():
                for v in i:
                    if v not in self._chars:
                        self._chars += v

    def tokenize(self,
                 numbers: bool = False,
                 words: bool = False,
                 only_keywords: bool = False,
                 strings: bool = False) -> list[Token]:
        """
        Processes the code passed to the constructor, breaking it into tokens.

        :param numbers: if True, the numbers will be processed and will be included in the final token list, otherwise not.
        :param words: if True, it will process those words that are not in the keywords argument passed to the constructor, otherwise it will not.
        :param only_keywords: if True, then words that are not in the keywords argument passed to the constructor will be ignored, otherwise not.
        :param strings: if True, will process the text in double quotes and add it to the final token list as a string token, otherwise not.
        :return: list[Token]
        """

        while self._pos < len(self._code):
            current = self._peek(0)

            if current.isdigit() and numbers:
                self._tokenize_number()
            elif current.isalpha() and words:
                self._tokenize_word(only_keywords)
            elif current in self._chars and self._operators is not ...:
                self._tokenize_operator()
            elif current == '"' and strings:
                self._next()
                self._tokenize_string()
            else:
                self._next()

        return self._tokens

    def _tokenize_number(self) -> None:
        result = ''
        current = self._peek(0)

        while current.isdigit() or current == '.':
            if '.' in result and current == '.':
                raise LexerError(f'incorrect float number "{result}".')

            result += current
            current = self._next()

        self._add_token('NUMBER', result)

    def _tokenize_operator(self) -> None:
        result = ''
        current = self._peek(0)

        while True:
            if result + current not in self._operators and result:
                self._add_token(self._operators[result], result)
                return

            result += current
            current = self._next()

    def _tokenize_word(self, only_keywords: bool) -> None:
        result = ''
        current = self._peek(0)

        while True:
            if not (current.isalpha() or current.isdigit()):
                break

            result += current
            current = self._next()

        if self._keywords is not ... and result in self._keywords:
            self._add_token(self._keywords[result], result)
        elif not only_keywords:
            self._add_token('WORD', result)

    def _tokenize_string(self) -> None:
        result = ''
        current = self._peek(0)

        while True:
            if current == '"':
                break

            result += current
            current = self._next()
        self._next()

        self._add_token('STRING', result)

    def _add_token(self, name: str, value: str) -> None:
        self._tokens.append(Token(name, value))

    def _peek(self, rel_pos: int) -> str:
        position = self._pos + rel_pos
        if position >= len(self._code):
            return '\0'
        return self._code[position]

    def _next(self) -> str:
        self._pos += 1
        return self._peek(0)
