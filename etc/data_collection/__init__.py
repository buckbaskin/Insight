import sys
from PTTRunner import Runner

def main():
    # test subsequence
    print("main start")
    r = Runner('test')
    r.user_search('a')
    print("main end")
    sys.exit(0)

print("init collecting")
main()
