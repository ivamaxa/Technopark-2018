import types


class Whenthen:
    def __init__(self, func):
        self.methods = []
        self.func = func
        self.num = -1

    def when(self, func):
        if self.methods[self.num]['then'] is None:
            raise ValueError
        self.methods.append({
            'when': func,
            'then': None
        })
        self.num += 1
        return self

    def then(self, func):
        if self.methods[self.num]['then'] is not None:
            raise ValueError
        self.methods[self.num]['then'] = func
        return self

    def __call__(self, elem):
        for el in self.methods:
            if el['when'](elem):
                return el['then'](elem)

        return self.func(elem)



