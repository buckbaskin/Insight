from tasks import intake_local_text

n = intake_local_text('pride.txt')
n = intake_local_text('war_of_the_worlds.txt', n)
n = intake_local_text('sawyer.txt', n)
print 'lll: '+str(len(n.vertices))
n.reduce_network(1, 1)
n.print_similarity()