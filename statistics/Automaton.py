from Reduce import Reduce
from Gather import Gather
from datetime import time
import datetime

import sys

if __name__ == '__main__':
    print('begin processing ->')
    
    
    f = open(r'/home/buck/Github/Insight/statistics/simile.smile','r')
    total_size = 16000
    file_size = 100
    index_num = input('beginning input for gather write, pretty please: ')
    
    start_time = datetime.datetime.now()
    
    g = Gather(option='happy',totalSize = total_size, fileSize = file_size,
                     consumerKey = f.readline()[:-1], consumerSecret = f.readline()[:-1],
                     accessToken = f.readline()[:-1], accessTokenSecret = f.readline())
    g.run(index_num)
    r = Reduce()
    path = r'/home/buck/Github/Insight/statistics/raw/'
    r.reduce(path,True)
    
    end_time = datetime.datetime.now()
    diff = end_time - start_time
    run_minutes = diff.total_seconds()/60
    
    print(str(total_size)+' tweets collected in '+str(run_minutes)+' minutes')
    print(' -> end processing. see happy.txt')
    sys.exit(0)