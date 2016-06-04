from Insight.service import server

print('importing service views')
@server.route('/data')
def data_response():
    return str(10101010)