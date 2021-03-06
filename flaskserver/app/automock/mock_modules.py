class Mock(object):
    pass

class JSMock(dict):
    pass

response = Mock()
response.status_code = 200
response.text = 'This is mock text'

mock_requests = Mock()
def get_function(string_):
    print('special string thing')
    print('s: '+string_)
    print('s: '+'http://127.0.0.1:5001')
    print('b? '+str(string_ == 'http://127.0.0.1:5001'))
    if string_ == 'http://127.0.0.1:5001':
        response.text = 'This is mock text'
        return response
    else:
        response.text = 'Default mock'
        return response

mock_requests.get = get_function

mock_time = Mock()
def sleep_function(time):
    return None
mock_time.sleep = sleep_function

jsmock = JSMock()
jsmock.mouseevent = JSMock()
jsmock.mouseevent['clientX'] = 10
jsmock.mouseevent['clientY'] = 10
jsmock.mouseevent['timeStamp'] = 50

jsmock.window = JSMock()
jsmock.window['location'] = JSMock()
jsmock.window['location']['pathname'] = '/'

