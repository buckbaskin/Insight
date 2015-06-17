from Collector import WordAssociation

wa = WordAssociation()

# f = open(wa.full_file_path('robotics'),'r')
for i in range(0,10):
    wa.collect_one('robotics')

print "results:\n"+str(wa.search('robotics'))+"\nend results"