'''
Test the javascript functions that are being run on the client side
'''
import execjs
import os

from Insight.app import server as flask_app
from Insight.service import server as flask_service

from Insight.automock import jsmock
from nose.plugins.skip import SkipTest
from nose.tools import ok_, assert_equal, assert_is_not_none
from nose.tools import timed

ctx = None
node = None

def setup_module():
    global node, ctx
    node = execjs.get(execjs.runtime_names.Node)
    with open('app/static/js/click.js', 'r') as clickjs_file:
        code = ''.join([str(line) for line in clickjs_file])
        test_code = ''
        with open('app/local/js/tests.js', 'r') as testjs_file:
            test_code = ''.join([str(line) for line in testjs_file])
        mock_code = ''
        with open('app/local/js/mocks.js', 'r') as mockjs_file:
            mock_code = ''.join([str(line) for line in mockjs_file])
        code += '\n\n'+test_code
        code += '\n\n'+mock_code
        ctx = node.compile(code)

def teardown_module():
    pass

def test_tests_included():
    assert_is_not_none(ctx)
    ok_(ctx.call('truth', 1))
    # ok_(not ctx.call('falsey', 1))

def test_mocks_included():
    # assert_is_not_none(ctx)
    ok_(ctx.eval('window.location.pathname === "/"'))

def test_js_setup():
    # assert_is_not_none(ctx)
    ok_(ctx.eval('isFunction(c)'))

@SkipTest
@timed(.1)
def test_small_compile():
    assert_is_not_none(ctx)
    document = 1
    window = 2
    xhr = 3
    debug = True
    assert_is_not_none(ctx.call('c', jsmock.mouseevent))
    assert_equal(200, 200)

