class Lexer:
    def __init__(self, code):
        self.code = code      # the raw source code string
        self.pos = 0          # current position we're reading
        self.tokens = []      # list of tokens we're building

    def current_char(self):
        # return the character at self.pos
        # return None if we've reached the end
        return self.code[self.pos] if self.pos < len(self.code) else None
        pass

    def advance(self):
        # move self.pos forward by 1
        self.pos += 1
        pass

    def tokenize(self):
        # main loop — keep reading until end of code
        # for each character, decide what token to make
        while self.current_char() is not None:
            char = self.current_char()
            if char.isspace():
                self.advance()  # skip whitespace
            elif char.isdigit():
                self.tokens.append(self.tokenize_number())
            elif char.isalpha() or char == '_':
                self.tokens.append(self.tokenize_identifier())
            elif char == '"':
                self.tokens.append(self.tokenize_string())
            elif char in '+-*/=(){}<>!':
                self.tokens.append(self.tokenize_operator())
            else:
                raise Exception(f"Unexpected character: {char}")
        pass