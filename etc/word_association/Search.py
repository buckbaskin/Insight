from Collector import AssociationLookup

class AssociationSearch(object):
    def __init__(self, add_lookup=False, lookups=1):
        self.lookup = (not (not add_lookup))
        self.lookups = lookups
        if self.lookup:
            self.al = AssociationLookup()
            
    def read_in(self, open_file):
        data = dict()
        # print "read in started"
        for line in open_file.readlines():
            # print line
            try:
                word, count = line.split('|')
            except ValueError:
                print "failed to include line: "+str(line).rstrip("\n")+" split: "+str(line.split('|'))
            data[word] = int(count.rstrip('\n'))
        # print "read in ended"
        return data
    
    def add_content(self, content, weight, content_dict):
        try:
            key = self.key_clean(str(content)).lower()
            if(self.invalid_key(key.lower())):
                return
        except:
            return
        try:
            data = int(content_dict[key.lower()])
        except KeyError:
            content_dict[key.lower()] = 0
            data = int(content_dict[key.lower()])
        try:
            content_dict[key.lower()] = int(data) + int(weight)
        except Exception as e:
            print e
            print "key: "+str(key.lower())+" data: "+str(data)+" weight: "+str(weight)
            raise(e)
    
    def search(self, text, max_items=100):
        if(self.lookup):
            for i in xrange(0,self.lookups):
                self.al.collect_one(text)
        tokens = text.split() # tokens in search
        terms = dict()
        for token in tokens:
            terms[token.lower()]=1
        # print 'begin processing search'
        for item in tokens:
            for association in self.process_one(item, max_items):
                # print "association: "+str(association)
                self.add_content(association[0],association[1], terms)
        for i in xrange(0,len(tokens)-2):
            pair = tokens[i]+" "+tokens[i+1]
            for association in self.process_one(pair, max_items):
                self.add_content(association[0],association[1], terms)
        
        for token in tokens:
            del terms[token.lower()]
        # print 'end processing search'
        for item in self.dict_by_value(terms):
            if(len(item[0])>3):
                tokens.append(item[0])
        # add everything back to the tokens list
        
        # list is sorted by terms, and then most associated terms
        if len(tokens) > max_items:
            return tokens[0:max_items]
        else:
            return tokens
    
    def process_one(self, term, max_items=100):
        try:
            f = open(self.full_file_path(term),'r')
        except IOError:
            f = open(self.full_file_path(term),'w')
            f.close()
            f = open(self.full_file_path(term),'r')
        associations = self.dict_by_value(self.read_in(f))
        if len(associations) > max_items:
            return associations[0:100]
        else:
            return associations
            
    def dict_by_value(self, dictionary):
        sorted_dict = sorted(dictionary.items(), key=lambda x: x[1], reverse=True) # sorts on the second item (value)
        # print "sorted_dict:"+str(sorted_dict)
        return sorted_dict
    
    def full_file_path(self, term):
        return ("data/"+term.replace(" ","_")+"_association.txt").lower()
    
    def invalid_key(self, key):
        if(len(key)<=2):
            return True
        baddies = ['the', 'camp', 'filth','that','they','like']
        for check in baddies:
            if(check == key):
                return True
        bad_parts = ['1','2','3','4','5','6','7','8','9','0','"',"'","[","@","#","&amp;","porn","http","t.co"]
        for check in bad_parts:
            if check in key:
                return True
        return False
    
    def key_clean(self, key):
        mod_key = key.replace("@","").replace("#","").replace("[","").replace("]","").replace("'","").replace("\"","").lower()
        mod_key = mod_key.replace(",","").replace("?","").replace(":","").replace("http://","").replace("https://","").lower()
        mod_key = mod_key.replace("!","").replace(".","").replace("-","")
        return mod_key

