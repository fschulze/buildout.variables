from buildout.variables import Recipe
import json
import pytest


def test_str():
    name = 'variables'
    options = {
        'foo1': 'str "ham-egg"',
        'foo2': 'str "ham-egg" [^a-z]',
        'foo3': 'str "ham-egg" [^a-z] _',
        'foo4': "str 'ham egg'",
        'foo5': 'str "ham egg"',
        'foo6': 'str ham',
        'foo7': 'str ham [a]',
        'foo8': 'str ham [a] _'}
    buildout = {name: options}
    Recipe(buildout, name, options).install()
    assert options['foo1'] == 'ham-egg'
    assert options['foo2'] == 'hamegg'
    assert options['foo3'] == 'ham_egg'
    assert options['foo4'] == 'ham egg'
    assert options['foo5'] == 'ham egg'
    assert options['foo6'] == 'ham'
    assert options['foo7'] == 'hm'
    assert options['foo8'] == 'h_m'


def test_int_and_new():
    name = 'variables'
    options = {
        'foo1': 'int 10',
        'foo1-c': 'new foo1',
        'foo1-b': 'new foo1',
        'foo1-a': 'new foo1',
        'foo2': 'int 2:10',
        'foo2-c': 'new foo2',
        'foo2-b': 'new foo2',
        'foo2-a': 'new foo2'}
    buildout = {name: options}
    Recipe(buildout, name, options).install()
    assert options['foo1'] == 'int 10'
    assert options['foo1-a'] == '0'
    assert options['foo1-b'] == '1'
    assert options['foo1-c'] == '2'
    assert options['foo2'] == 'int 2:10'
    assert options['foo2-a'] == '2'
    assert options['foo2-b'] == '3'
    assert options['foo2-c'] == '4'


def test_int_and_indexed():
    name = 'variables'
    options = {
        'index-key': 'ham',
        'foo1': 'indexed 1{index}0',
        'foo2': 'int foo1 2',
        'foo2-a': 'new foo2',
        'foo2-b': 'new foo2'}
    buildout = {name: options}
    Recipe(buildout, name, options).install()
    assert options['foo1'] == '110'
    assert options['foo2'] == 'int foo1 2'
    assert options['foo2-a'] == '110'
    assert options['foo2-b'] == '111'


def test_index_start():
    name = 'variables'
    options = {
        'index-key': 'ham',
        'index-start': '100',
        'foo': 'indexed ham-{index}'}
    buildout = {name: options}
    Recipe(buildout, name, options).install()
    assert options['foo'] == 'ham-100'


def test_unknown_op():
    name = 'variables'
    options = {
        'foo': 'bar ham'}
    buildout = {name: options}
    pytest.raises(ValueError, Recipe, buildout, name, options)


def test_index_file_created(tmpdir):
    name = 'variables'
    foo_json = tmpdir.join('foo.json')
    options = {
        'index-file': unicode(foo_json)}
    buildout = {name: options}
    assert not foo_json.check()
    Recipe(buildout, name, options).install()
    assert foo_json.check()
    with open(unicode(foo_json)) as f:
        assert json.load(f) == {}


def test_persisted_index(tmpdir):
    name = 'variables'
    foo_json = tmpdir.join('foo.json')
    options = {
        'index-key': 'bar1',
        'index-file': unicode(foo_json),
        'foo': 'indexed ham-{index}'}
    buildout = {name: options}
    Recipe(buildout, name, options).install()
    assert options['foo'] == 'ham-1'
    # another key should generate a new index
    options = {
        'index-key': 'bar2',
        'index-file': unicode(foo_json),
        'foo': 'indexed ham-{index}'}
    buildout = {name: options}
    Recipe(buildout, name, options).install()
    assert options['foo'] == 'ham-2'
    # using the same key again, should give us the same index
    options = {
        'index-key': 'bar1',
        'index-file': unicode(foo_json),
        'foo': 'indexed ham-{index}'}
    buildout = {name: options}
    Recipe(buildout, name, options).install()
    assert options['foo'] == 'ham-1'
    # check the file
    with open(unicode(foo_json)) as f:
        assert json.load(f) == {u'bar1': 0, u'bar2': 1}
    # but the index-start is always added
    options = {
        'index-key': 'bar2',
        'index-start': '100',
        'index-file': unicode(foo_json),
        'foo': 'indexed ham-{index}'}
    buildout = {name: options}
    Recipe(buildout, name, options).install()
    assert options['foo'] == 'ham-101'
