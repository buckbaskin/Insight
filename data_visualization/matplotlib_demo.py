import matplotlib.pyplot as plot
from numpy.random import rand
'''
for color in ['red','green','blue']:
    n = 10
    x,y = rand(2,n)
    scale = 200.0*rand(n)
    plot.scatter(x, y, s=scale, c=color, alpha= 1,label=color,edgecolors = 'none')
'''
for integer in range(0,10):
    n=20
    x,y= (100-(10-integer)*2)*rand(2,n)+(10-integer)
    scale = 50
    plot.scatter(x=x, y=y, s=scale, c='red', alpha = (integer*1.1)/(11.0), edgecolors = 'none')
    
'''
n = 500
x1,y1 = 400*rand(2,n)
scale = 50
plot.scatter(x=x1, y=y1, s=scale, c='red', alpha = .5,label = 'red',edgecolors = 'none')

x2,y2 = 400*rand(2,n)
plot.scatter(x=x2,y=y2,s=scale,c='green', alpha = 1, label = 'green',edgecolors = 'none')
'''

#plot.grid(True)
plot.show()