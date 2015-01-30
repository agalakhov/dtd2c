#!/usr/bin/python

class BnfParser:

    def __init__(self, bnf=None):
        if bnf is not None:
            self.parse(bnf)

    def parse(self, bnf):
        bnf = bnf.replace("(", " ( ").replace(")", " ) ")
        bnf = bnf.replace(",", " , ").replace("|", " | ")
        bnf = bnf.replace("?", " ? ").replace("*", " * ")
        tokens = bnf.split()
        result, tokens = self.__descend(tokens)
        if len(tokens) > 0:
            raise Exception("Syntax error at token " + tokens[0])
        print(result)

    # private

    def __descend(self, tokens):
        return self.__p_expr(tokens, ",", self.__p_expr, "|", self.__p_atom)

    def __p_expr(self, tokens, char, call, *args, **kwargs):
        t, tokens = call(tokens, *args, **kwargs)
        result = [ t ]
        while len(tokens) > 0 and tokens[0] == char:
            t, tokens = call(tokens[1:], *args, **kwargs)
            result.append(t)
        if len(result) == 1:
            result = result[0]
        else:
            result = tuple([char] + result)
        return result, tokens

    def __p_atom(self, tokens):
        if tokens[0] == "(":
            result, tokens = self.__descend(tokens[1:])
            if tokens[0] != ")":
                raise Exception("Syntax error: expected ')', got " + tokens[0])
            tokens.pop(0)
        else:
            result, tokens = tokens[0], tokens[1:]
        if len(tokens) > 0:
            for char in "*?":
                if tokens[0] == char:
                    tokens.pop(0)
                    result = (char, result )
                    break
        return result, tokens

def parse(bnf):
    BnfParser(bnf)
