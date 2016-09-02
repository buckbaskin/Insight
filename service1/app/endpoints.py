from app import server

@server.route('/data')
def data_response():
    return str(10101010)
