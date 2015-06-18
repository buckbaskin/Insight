from Search import AssociationSearch
import sys

augment = (not(not(input("Augment search with new results? "))))
if augment:
    augment_depth = int(input("Number of augmentations: "))
else:
    augment_depth = 0

results = int(input("Number of results: "))

ass = AssociationSearch(augment, augment_depth)

while(True):
    a = raw_input("search: ")
    if str(a) is str("exit"):
        sys.exit(0)
    print "results:\n"+str(ass.search(a, results))+"\nend results"