# from stackoverflow/questions/.../generating-a-dense-matrix-from-a-sparse-matrix-in-numpy-python
# from scipy.sparse import csr_matrix

# A = csr_matrix([1,0,2],[0,3,0])

# print A

# print A.todense()

# print A.toarray()

# row = 0
# max_ = 10

def estimated_connection(prev, current):
    # prev, current = dictionaries of posts, weights, times, etc for two users
    # returns the likelihood of the current data coming from the prev data
    # this is primarily based on timing and metadata between the two
    #  not an analysis of weights and other nodes
    return prev[current['posts'][0].username]] + .1

data = dict()

while item in stream:
    if not relevant(item):
        continue

    if item.username not in data:
        data[item.username] = {}
        data[item.username]['posts'] = []
    
    data[item.username]['posts'].append(item)

    for key, value in data.iteritems():
        if not key == item.username:
            data[key][item.username] = estimated_connection(data[key], data[item.username])