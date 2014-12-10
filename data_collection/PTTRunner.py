from data_collection.PTTInterface import PTTInterface
import collections
import os
class Runner():
    
    def __init__(self, output_file_base):
        global output_base
        output_base = output_file_base
        global interface
        interface = self.createInterface()
        
    
    def createInterface(self):
        f = open(r'/home/buck/Github/Insight/data_collection/simile.smile','r')
        return PTTInterface(f.readline()[:-1],f.readline()[:-1],f.readline()[:-1],f.readline(),
                            output_base,2,50)
    
    def run(self):
        test_type = input('Search:True :: Stream:False -> ')
        if(test_type):
            interface.search(query=self.get_search_input())
        else:
            interface.search(query=self.get_stream_input())

    def get_search_input(self):
        #parse keyword input by splitting on the commas
        unparsed_input = raw_input('Please choose search query -> ')
        return unparsed_input
    def search(self,q):
        return interface.search(query=q)

    def user_search(self,q):
        return interface.user_search(q)

    def get_stream_input(self):
        #parse keyword input by splitting on the commas
        unparsed_input = raw_input('Please choose stream query -> ')
        return unparsed_input

'''
class AutoRunner():
    
    def __init__(self):
        global interface
        interface = self.createInterface()
        
    def createInterface(self):
        f = open('simile.smile','r')
        return PTTInterface(f.readline()[:-1],f.readline()[:-1],f.readline()[:-1],f.readline(),
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
                
                '''