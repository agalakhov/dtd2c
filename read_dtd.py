#!/usr/bin/python

from collections import OrderedDict as odict

import ebnf

class Element:

    def __init__(self, bnf):
        self.bnf = ebnf.parse(bnf)
        self.attlist = odict()

    def set_attlist(self, attlist):
        for (n, v, t) in attlist:
            self.attlist[n] = (v, t)

    def __repr__(self):
        return "tag<[{}] {}>".format(self.bnf, str(self.attlist))


class Parser:

    def __init__(self, data=None):
        self.entities = odict()
        self.elements = odict()
        if data is not None:
            self.parse(data)

    def parse(self, data):
        c = 0
        while c < len(data):
            s = data.find(b"<!", c)
            if s == -1:
                s = len(data)
            if len(data[c:s].strip()) != 0:
                raise Exception("Junk between tags at pos " + str(c))
            if s == len(data):
                break
            comment = (data[s : s + 4] == b"<!--")
            if comment:
                e = data.find(b"-->", s + 2) + 2
            else:
                e = data.find(b">", s)
            if e == -1:
                raise Exception("Tag not closed at pos " + str(s))
            if not comment:
                self.__process_tag(data[s + 2 : e].decode())
            c = e + 1

    # private

    def __process_tag(self, tag):
        data = tag.rstrip().split(maxsplit=2)
        if len(data) != 3:
            raise Exception("Tag is invalid: " + tag)
        t, n, v = data
        if t == "ENTITY":
            if n == "%":
                data = v.split(maxsplit=1)
                if len(data) != 2:
                    raise Exception("Entity is invalid: " + tag)
                n, v = data
                if v[0] != '"' or v[-1] != '"':
                    raise Exception("Parameter entity value is not quoted: " + tag)
                self.__process_p_entity(n, v[1:-1])
            else:
                raise Exception("Sorry, non-parameter entities are not implemented yet")
        elif t == "ELEMENT":
            self.__process_element(n, v)
        elif t == "ATTLIST":
            self.__process_attlist(n, v)
        else:
            raise Exception("Unknown tag type " + t)

    def __process_element(self, name, value):
        self.elements[name] = Element(value)

    def __process_attlist(self, name, value):
        attrs = value.split()
        if len(attrs) % 3 != 0:
            raise Exception("Attribute list is invalid: " + str(attrs))
        attrs = [ (attrs[i], attrs[i + 1], attrs[i + 2]) for i in range(0, len(attrs), 3) ]
        if name not in self.elements:
            raise Exception("No such element: " + name)
        self.elements[name].set_attlist(attrs)


    def __process_p_entity(self, name, value):
        self.entities[name] = value

def parse(data):
    p = Parser(data)



if __name__ == "__main__":
    from sys import argv
    parse(open(argv[1], "rb").read())
