# the package for my statistics project
from Gather import Gather
import sys

f = open(r'/home/buck/Github/Insight/statistics/simile.smile','r')
g = Gather(option='happy',totalSize = 20, fileSize = 10,
                 consumerKey = f.readline()[:-1], consumerSecret = f.readline()[:-1],
                 accessToken = f.readline()[:-1], accessTokenSecret = f.readline())
g.run(1)
print('end in main run')
sys.exit(0)