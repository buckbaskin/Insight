
from follow_tree import FollowTree

def traverse(root, string):
    if(len(root.tree_followers)):
        for child in root.tree_followers:
            traverse(child, string+' '+root.user)
    else:
        print string+' '+root.user

def main():
    f = FollowTree('1463250931')
    f.build()
    print ' >>> traverse started: '
    traverse(f.root, 'interest path: ')
    print ' <<< end traverse'
    exit()

if __name__ == '__main__':
    main()