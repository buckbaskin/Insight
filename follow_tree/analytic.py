
from follow_tree import FollowTree
import time

def traverse(root, string):
    if(len(root.tree_followers)):
        for child_id in root.tree_followers:
            child = root.tree_followers[child_id]
            print 'child.__class__ >> '+str(child.__class__)
            traverse(child, string+' '+root.user)
    else:
        print string+' end '+root.user

def main():
    print 'create FollowTree'
    f = FollowTree('1463250931')
    print 'build:'
    f.build()
    print 'wait for build'
    time.sleep(30)
    print 'end sleep for build'
    print ' >>> traverse started: '
    print 'f.root.__class__ > '+str(f.root.__class__)
    traverse(f.root, 'interest path 1: ')
    print ' <<< end traverse'
    time.sleep(30)
    traverse(f.root, 'interest path 2: ')

if __name__ == '__main__':
    main()