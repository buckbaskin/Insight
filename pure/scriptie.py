from Insight.pure.decorator import force_pure, check_pure
import pdb

class Dan(object):
    def __init__(self):
        self.x = 1

def randomness(a):
    # a.vimmer = 'Jamison'
    pass

randomness = check_pure(randomness)

print('randomness()? '+str(randomness(Dan())))

