
from follow_tree import FollowTree
import time

def traverse(root, string):
    if(len(root.tree_followers)):
        for child in root.tree_followers:
            print 'child.__class__ >> '+str(child.__class__)
            traverse(child, string+' '+root.user)
    else:
        print string+' '+root.user

def main():
    f = FollowTree('1463250931')
    f.build()
    print 'begin sleep'
    time.sleep(1)
    print 'sleeping.'
    time.sleep(1)
    print 'sleeping..'
    time.sleep(1)
    print 'sleeping...'
    time.sleep(1)
    print 'sleeping....'
    time.sleep(1)
    print 'sleeping.....'
    time.sleep(1)
    print 'end sleep'
    print ' >>> traverse started: '
    print 'f.root.__class__ > '+str(f.root.__class__)
    traverse(f.root, 'interest path: ')
    print ' <<< end traverse'
    exit()

if __name__ == '__main__':
    main()