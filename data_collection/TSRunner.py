from data_collection import TwitterSearchInterface
import collections
import os

class Runner():
    
    def __init__(self):
        global interface
        interface = self.createInterface()
    
    def createInterface(self):
        f = open('simile.smile','r')
        return PTTInterface(f.readline()[:-1],f.readline()[:-1],f.readline()[:-1],f.readline(),'test',1)
    
    def run(self):
        interface.query(interface.get_input())

class AutoRunner():
    
    def __init__(self):
        global interface
        interface = self.createInterface()
        
    def createInterface(self):
        f = open('simile.smile','r')
        return TwitterSearchInterface(f.readline()[:-1],f.readline()[:-1],f.readline()[:-1],f.readline(),
                                'auto',2)
    
    def make_input(self):
        #parse keyword input by splitting on the commas
        output_set = list()
        with open(r'input/search_list.txt','r') as f:
#            print(os.path.abspath(f.name))
            for line in f:
#                print("line: "+line)
                input_set = collections.namedtuple('input', ['keywords','modifiers'])
                output_set.append(input_set(line.split(','),['en' , 100, False]))
        f.close()
        return output_set
    
    def run(self):
        input_set = self.make_input()
#        print("inputs: "+str(input_set))
        no_overload = True
        for i in input_set:
            no_overload = interface.query(i)
            if(no_overload == False):
                print('check for Rate Limit Error')
                break