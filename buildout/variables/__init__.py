import json
import os
import re
import rsfile


class VariableError(Exception):
    pass


class OpIndexed(object):
    def __init__(self, data):
        self.value = data.strip()

    def __call__(self, buildout, lookup):
        return self.value.format(index=lookup['index'])

    def next(self, buildout, lookup):
        return self.value.format(index=lookup['index'])


class OpInt(object):
    def __init__(self, data):
        try:
            b, r = data.split(None, 1)
        except ValueError:
            r = data
            b = 0
        r = [int(x) for x in r.split(':', 2)]
        self.base = b
        self.range = iter(range(*r))

    def next(self, buildout, lookup):
        try:
            base = int(self.base)
        except ValueError:
            base = int(lookup[self.base].next(buildout, lookup))
        return str(base + self.range.next())


class OpNew(object):
    def __init__(self, data):
        self.value = data.strip()

    def __call__(self, buildout, lookup):
        return lookup[self.value].next(buildout, lookup)


class OpStr(object):
    def __init__(self, data):
        if data[0] in '\'"':
            index = data[1:].index(data[0]) + 1
            s = data[1:index]
            sub = data[index + 1:].strip()
        else:
            try:
                s, sub = data.split(None, 1)
            except ValueError:
                s = data
                sub = ''
        try:
            sub, repl = sub.rsplit(None, 1)
        except ValueError:
            repl = ''
        if sub:
            self.value = re.sub(sub, repl, s)
        else:
            self.value = s

    def __call__(self, buildout, lookup):
        return self.value


class Variables(object):
    _ops = dict(
        indexed=OpIndexed,
        int=OpInt,
        new=OpNew,
        str=OpStr)

    def __init__(self):
        self.callables = dict()
        self.lookup = dict()

    def add(self, name, value):
        try:
            op, data = value.split(None, 1)
        except ValueError as e:
            raise VariableError(e)
        try:
            op = self._ops[op]
        except KeyError:
            raise ValueError("Unknown operator '%s'" % op)
        op = op(data)
        if callable(op):
            self.callables[name] = op
        if hasattr(op, 'next'):
            self.lookup[name] = op

    def evaluate(self, buildout, name, options):
        for k, v in sorted(self.callables.items()):
            options[k] = v(buildout, self.lookup)


class Recipe(object):
    def __init__(self, buildout, name, options):
        variables = Variables()
        data = {}
        if options.get('index-file'):
            if os.path.exists(options['index-file']):
                with rsfile.rsopen(options['index-file']) as f:
                    data = json.load(f)
        key = options.get('index-key')
        if key is not None:
            if key not in data:
                data[key] = len(data)
            index_start = int(options.get('index-start', 1))
            variables.lookup['index'] = data[key] + index_start
        if options.get('index-file'):
            with rsfile.rsopen(options['index-file'], 'wb') as f:
                json.dump(data, f, indent=4)
        for k, v in options.items():
            try:
                variables.add(k, v)
            except VariableError:
                continue
        variables.evaluate(buildout, name, options)

    def install(self):
        pass
