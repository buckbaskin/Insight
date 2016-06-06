class Mock(object):
    pass

response = Mock()
response.status_code = 200
response.text = 'This is mock text'

mock_requests = Mock()
def get_function(string_):
    print('special string thing')
    if string_ == 'http://127.0.0.1:5001':
        return response
    return response

mock_requests.get = get_function

mock_time = Mock()
def sleep_function(time):
    return None
mock_time.sleep = sleep_function
