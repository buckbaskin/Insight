from os import listdir
from copy import copy

class Reduce():
    
    def __init__(self):
        pass
    
    def reduce(self, path, reset):
        filenames = listdir(path)
        happy_file = path+'happy.txt'
        if(reset == False):
            pass #collect old info if available first, then append info
        happy_list = []
        for f in filenames:
            if len(f)>=6 and f[0:5]=="happy" and f[5]!='.':
                print('file:'+str(f))
                for line in open(path+f):
                    splits = line.split(" ")
                    for element in splits:
                        mod_e = element
                        mod_e = mod_e.strip()
                        mod_e = mod_e.translate(None,'"')
                        mod_e = mod_e.translate(None,'#')
                        if(len(mod_e)>2):
                            if mod_e[1] == '(':
                                mod_e = mod_e[1:]
                            if mod_e[-1] == ')':
                                mod_e = mod_e[:-1]
                        if(len(mod_e)>1):
                            happy_list.append(mod_e)
        print('----------')
        happy_list.sort()
        # process list for duplicates
        # - process into a list of tuples
        # - sort the tuples by number
        # - write to file -> [string]|[frequency]
        happy_complete = []
        max_count = 5
        count = 0
        for index in range(0,len(happy_list)):
            if(index+1 < len(happy_list)):
                #print('[i]'+happy_list[index]+' [i+1]'+happy_list[index+1])
                if happy_list[index].lower() == happy_list[index+1].lower():
                    count = count+1
                else:
                    if(len(happy_list[index])> 0):
                        happy_complete.append((copy(happy_list[index]),copy(count+1)))
                    if(count > max_count and (not ')' in happy_list[index] and
                                         not '(' in happy_list[index] and not 'RT'  in happy_list[index]
                                         and not ':D'  in happy_list[index] and not ':-'  in happy_list[index])):
                        #boolean_test = (not ')' in happy_list[index] and not '(' in happy_list[index])
                        #boolean_test2 = (not ':)' in happy_list[index])
                        #print('potential max: '+happy_list[index]+' w/ max '+str(count)+' with boolean count '+str(boolean_test2))
                        max_count = copy(count)
                    count = 0
        with open(happy_file,'w') as happy:
            for item in happy_complete:
                try:
                    happy.write(item[0].encode('utf-8')+'|'+str(item[1]).encode('utf-8')+'\n')
                except Exception as e:
                    fixed = False
                    try:
                        uni = item[0][:-3]
                        if(len(uni)>0):
                            #print('try: '+uni)
                            happy.write(uni.encode('utf-8')+'|'+str(item[1]).encode('utf-8')+'\n')
                            fixed = True
                    except Exception as ee:
                        pass
                    try:
                        if fixed == False:
                            uni = item[0][3:]
                            if(len(uni)>0):
                                #print('try: '+uni)
                                happy.write(uni.encode('utf-8')+'|'+str(item[1]).encode('utf-8')+'\n')
                                fixed = True
                    except Exception as ee:
                        pass
                    try:
                        if fixed == False:
                            uni = item[0][:-4]
                            if(len(uni)>0):
                                #print('try: '+uni)
                                happy.write(uni.encode('utf-8')+'|'+str(item[1]).encode('utf-8')+'\n')
                                fixed = True
                    except Exception as ee:
                        pass
                    if (fixed == False):
                        print(''+item[0]+' is a failed character')
                        #print('item[1] '+str(item[1]))
                        #print(e)
        happy.close()
        print('max_count = '+str(max_count))
        #print("end happy file write")

def test():
    r = Reduce()
    path = r'/home/buck/Github/Insight/statistics/raw/'
    r.reduce(path,True)

if __name__ == '__main__':
    print('test Reduce')
    test()
    print('end test Reduce ')