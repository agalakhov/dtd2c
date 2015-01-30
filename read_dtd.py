#!/usr/bin/python

class Parser:

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
                self.__process_tag(data[s + 2 : e])
            c = e + 1

    # private

    def __process_tag(self, tag):
        data = tag.rstrip().split(maxsplit=2)
        if len(data) != 3:
            raise Exception("Tag is invalid: " + str(tag))
        t, n, v = data
        if t == b"ENTITY":
            if n == b"%":
                data = v.split(maxsplit=1)
                if len(data) != 2:
                    raise Exception("Entity is invalid: " + str(tag))
                n, v = data
                if v[0] != 34 or v[-1] != 34: # 34 = ord "
                    raise Exception("Parameter entity value is not quoted: " + str(tag))
                self.__process_p_entity(n, v[1:-1])
            else:
                raise Exception("Sorry, non-parameter entities are not implemented yet")
        elif t == b"ELEMENT":
            self.__process_element(n, v)
        elif t == b"ATTLIST":
            self.__process_attlist(n, v)
        else:
            raise Exception("Unknown tag type " + str(t))

    def __process_element(self, name, value):
#        print("Declare element " + str(name) + " as " + str(value))
        pass

    def __process_attlist(self, name, value):
        attrs = value.split()
        if len(attrs) % 3 != 0:
            raise Exception("Attribute list is invalid: " + str(attrs))
        attrs = [ (attrs[i], attrs[i + 1], attrs[i + 2]) for i in range(0, len(attrs), 3) ]
        print("Declare attlist " + str(name) + " as ", attrs)


    def __process_p_entity(self, name, value):
#        print("Declare entity " + str(name) + " as " + str(value))
        pass

def parse(data):
    Parser().parse(data)



if __name__ == "__main__":
    from sys import argv
    parse(open(argv[1], "rb").read())
