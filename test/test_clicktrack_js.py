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
    with open('app/templates/js/components/click.js', 'r') as clickjs_file:
        code = ''.join([str(line) for line in clickjs_file])
        test_code = ''
        with open('app/local/js/tests.js', 'r') as testjs_file:
            test_code = ''.join([str(line) for line in testjs_file])
        mock_code = ''
        with open('app/local/js/mocks.js', 'r') as mockjs_file:
            mock_code = ''.join([str(line) for line in mockjs_file])
        ok_code = ''
        with open('app/local/js/ok.js', 'r') as ok_file:
            ok_code = ''.join([str(line) for line in ok_file])
        code += '\n\n'+test_code
        code += '\n\n'+mock_code
        code += '\n\n'+ok_code
        ctx = node.compile(code)

def teardown_module():
    pass

def test_tests_included():
    assert_is_not_none(ctx)
    ok_(ctx.call('truth', 1))
    # ok_(not ctx.call('falsey', 1))

def test_mocks_included():
    ok_(ctx.eval('window.location.pathname === "/"'))

def test_js_setup():
    ok_(ctx.eval('isFunction(click.loadm)'))

def test_ok_included():
    ok_(ctx.eval('isFunction(ok)'))

@SkipTest
@timed(.1)
def test_small_compile():
    document = 1
    window = 2
    xhr = 3
    debug = True
    assert_is_not_none(ctx.call('c', jsmock.mouseevent))

def test_demo_okjs_positive():
    # 0 is okay, 1 is assertion, -1 is other error
    assert_equal(ctx.eval('ok(assert.ok, true)'), 0)

def test_demo_okjs_negative():
    assert_equal(ctx.eval('ok(assert.ok, false)'), 1)

def test_demo_okjs_error():
    assert_equal(ctx.eval('ok(function () { throw new Error("test fail") }, 0)'), -1)

