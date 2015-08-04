import numpy
import math
import copy

class SVD_Process(object):
    '''Create a class that creates and maintains the SVD for a matrix
    
    Use:
        svd = SVD_Process()
        svd.pass_new_data(data_array, x_labels, y_labels)
            -> data array is a numpy array
            -> x_labels, y_labels are lists of strings
            <- no value returned
        svd.process_data()
            -> no inputs
            $$ performs svd, and reordering
            <- no value returned
        svd.current_('w')
            -> string with data requested (ex. the W array from SVD)
            # options: data_array, x_labels, y_labels, W,U,V (None if invalid)
            <- returns data (ex. the W array from the SVD)
            
    
    '''
    
    
    def __init__(self):
        #  data storage. Data is added through helper methods
        global data_array
        data_array = numpy.zeros(1,1)
        global x_labels
        x_labels = [ "" ]
        global y_labels
        y_labels = [ "" ]
        
        #  results
        # from input data_array as A
        # A decomposed to A => U * W * Vtranspose
        # U, V are matrices
        # W is a vector
        global W
        W = []
        global U
        U = numpy.zeros(1,1)
        global V
        V = numpy.zeros(1,1)
        
        # dimensions of the input 
        global n
        n = 1
        global m
        m = 1
        
        # other info
    
    def pass_new_data(self, dataArray, xLabels, yLabels):
        try:
            if(dataArray is not None and xLabels is not None and yLabels is not None):
                global data_array
                data_array = dataArray
                shape = data_array.shape
                global m
                m = shape[0]
                global n
                n = shape[1]
                global x_labels
                x_labels = xLabels
                global y_labels
                y_labels = yLabels
                
                #clear prior solutions
                global W
                W = []
                global U
                U = numpy.zeros(1,1)
                global V
                V = numpy.zeros(1,1)
        
                return 1
            else:
                return 0
        except Exception:
            return -1
    
    def current_(self,vari):
        if vari == "data_array":
            global data_array
            return data_array
        elif vari == "x_labels":
            global x_labels
            return x_labels
        elif vari == "y_labels":
            global y_labels
            return y_labels
        elif vari == "w":
            global W
            return W
        elif vari == "v":
            global V
            return V
        elif vari == "u":
            global U
            return U
        else:
            return None
    
    def process_data(self):
        self.decompose()
        self.reorder()
    
    #please note. method created after reading
    # Numerical Recipes "SVD Implementation" Webnote No. 2, Rev.1
    # http://www.nr.com/webnotes/nr3web2.pdf
    def decompose(self):
        '''
        Full Singular Value Decomposition
        '''
        # ***** SETUP *****
        global W
        global U
        global V
        global m
        global n
        flag = False
        eps = 1 #TODO - find out what EPS is 
        # indicies i, j, k, its
        j,l,nm = 0 , 0 , 0 , 0 , 0 , 0 , 0
        anorm,c,f,g,h,s,scale,x,y,z = 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0
        rv1 = [0.0] * n
        
        # ***** Householder Reduction to bidiagonal form *****
        # TODO start here
        for i in xrange(0,n):
            l = i+2
            rv1[i] = scale*g
            g= 0.0
            s= 0.0
            scale=0.0
            if(i < m):
                for k in xrange(i,m):
                    scale = scale + abs(U[k][i])
                if scale != 0:
                    for k in xrange(i,m):
                        U[k][i] = U[k][i] / scale
                        s = s + U[k][i] * U[k][i]
                        f = copy(U[i][i])
                        g = -1*self.SIGN(math.sqrt(s),f)
                        h = f*g-s
                        U[i][i] = f-g
                        for j in xrange(l-1,n):
                            s = 0.0
                            for k in xrange(i,m):
                                s = s + U[k][i]*U[k][j]
                            f = s/h
                            for k in xrange(i,m):
                                U[k][i] = U[k][i] * scale
            W[i] = scale * g
            g = 0.0
            s = 0.0
            scale = 0.0
            if(i+1 <= m and i+1 != n):
                for k in xrange(l-1,n):
                    scale = scale + abs(U[i][k])
                if scale != 0.0:
                    for k in xrange(l-1,n):
                        U[i][k] = U[i][k] / scale
                        s = s + U[i][k] * U[i][k]
                    f = U[i][l-1]
                    g = -1 * self.SIGN(math.sqrt(s),f)
                    h = f*g-s
                    U[i][l-1] = f-g
                    for k in xrange(l-1,n):
                        rv1[k] = U[i][k] / h
                    for j in xrange(l-1,m):
                        s = 0.0
                        for k in xrange(l-1,n):
                            s = s + U[j][k]*U[i][k]
                        for k in xrange(l-1,n):
                            U[j][k] = U[j][k] + s*rv1[k]
                    for k in xrange(l-1,n):
                        U[i][k] = U[i][k] * scale
            anorm = max(anorm, (abs(W[i])+abs(rv1[i])))
        
        # ***** Accumulation of right hand transformations *****
        #     remember double division
        for i in xrange(n-1,0,-1):
            if i < n-1:
                if g != 0.0:
                    for j in xrange(l,n):
                        V[j][i]  = ( U[i][j] / U[i][l] ) / g
                    for j in xrange(l,n):
                        s = 0.0
                        for k in xrange(l,n):
                            s = s + U[i][k] * V[k][j]
                        for k in xrange(l,n):
                            V[k][j] = V[k][j] + s*V[k][i]
                for j in xrange(l,n):
                    V[i][j] = 0.0
                    V[j][i] = 0.0
            V[i][i] = 1.0
            g = copy(rv1[i])
            l = copy(i)
        
        # ***** Accumulation of left hand transformations *****
        for i in xrange(min(m,n)-1,0,-1):
            l = i+1
            g = copy(W[i])
            for j in xrange(l,n):
                U[i][j] = 0.0
            if g != 0.0:
                g = 1.0/g
                for j in xrange(l,n):
                    s = 0.0
                    for k in xrange(l,m):
                        s = s + U[k][i] * U[k][j]
                    f = (s / U[i][i]) * g
                    for k in xrange(i,m):
                        U[k][j] = U[k][j] + f * U[k][i]
                for j in xrange(i,m):
                    U[j][i] = U[j][i] * g
            else: #g = 0.0
                for j in xrange(i,m):
                    U[j][i] = 0.0
            U[i][i] += 1
        
        # ***** Diagonalization of the bidiagonal form *****
        #    Loop over single values, and over allowed iterations
        #    remember test for splitting
        #    remember cancelation of rv1[1] if l > 0
        for k in xrange(n-1,0,-1):
            for its in xrange(0,30):
                flag = True
                for l in xrange(k,0,-1):
                    nm = l-1
                    if l == 0 or abs(rv1[l]) <= eps*anorm:
                        flag = False
                        break
                    if (abs(W[nm]) <= eps*anorm):
                        break
                if flag:
                    c = 0.0
                    s = 1.0
                    for i in xrange(l,k+1):
                        f = s*rv1[i]
                        rv1[i] = c*rv1[i]
                        if abs(f) <= eps*anorm:
                            break
                        g = copy(W[i])
                        h = self.dist(f,g)
                        W[i] = copy(h)
                        h = 1.0/h
                        c = g*h
                        s = -1*f*h
                        for j in xrange(0,m):
                            y = copy(U[i][nm])
                            z = copy(U[j][i])
                            U[j][nm] = y*c+z*s
                            U[j][i] = z*c-y*s
        
        # still in diagonalization                    
            z = copy( W[k] )
            # ***** Convergence (hopefully) *****
            #    Singular value is made non-negative
            #    remember Shift from bottom 2-by-2 minor
            #    remember next QR transformation
            #    remember rotation can be arbitrary if z = 0
            if l == k:
                if z < 0.0 :
                    W[k] = -z
                    for j in xrange(0,n):
                        V[j][k] = -V[j][k]
                break
            if its == 29:
                raise('No Convergence in 30 iterations for k = %i. Please [re]consider data' % k)
            x = copy(W[l])
            nm = k-1
            y = copy(W[nm])
            g = copy(rv1[nm])
            h = copy(rv1[k])
            f = ((y-z)*(y+z)+(g-h)*(g+h))/(2.0*h*y)
            g = self.dist(f,1)
            f = ((x-z)*(x+z)+h*((y/(f+self.SIGN(g,f)))-h))/x
            c = 1.0
            s = 1.0
            for j in xrange(l,nm):
                i = j+1
                g = copy(rv1[i])
                y = copy(W[i])
                h = s*g
                g = c*g
                z = self.dist(f,h)
                rv1[i] = z
                c = f/z
                s = h/z
                f = x*c+g*s
                g = g*c-x*s
                h = y*s
                y = y*c
                for jj in xrange(0,n):
                    x = copy(V[jj][j])
                    y = copy(V[jj][i])
                    V[jj][j]=x*c+z*s
                    V[jj][i]=z*c-x*s
                z = self.dist(f,h)
                W[j]  = copy(z)
                if z: # if z is not 0
                    z = 1/z
                    c = f*z
                    z = h*z
                f = c*g+s*y
                x = c*y-s*g
                for jj in xrange(0,m):
                    y = copy(U[jj][j])
                    z = copy(U[jj][i])
                    U[jj][j] = y*c+z*s
                    U[jj][i] = z*c-y*s
            rv1[l] = 0.0
            rv1[k] = copy(f)
            W[k] = copy(x)
    # end def decompose
        
        
    
    def reorder(self):
        '''
        Reorder the data in terms of decreasing magnitude. 
        Also, flip signs in columns to maximize positive elements
        
        operating on:
        [class] U , V , W
        '''
        # ***** SETUP *****
        global W
        global U
        global V
        global m
        global n
         
        inc = 1
        su = [0.0] * m
        sv = [0.0] * n
        
        # ***** SHELL SORT *****
        # do-while #1
        condition = True
        while(condition):
            inc *= 3
            inc += 1
            condition = (inc <= n)
        # end do-while #1
        # do-while #2
        condition = True
        while(condition):
            inc = inc/3
            for i in xrange(inc,n):
                sw = copy(W[i])
                for k in xrange(0,m):
                    su[k] = copy(U[k][i])
                for k in xrange(0,n):
                    sv[k] = copy(V[k][i])
                j = copy(i)
                while W[j-inc] < sw:
                    W[j] = copy(W[j-inc])
                    for k in xrange(0,m):
                        U[k][j] = copy(U[k][j-inc])
                    for k in xrange(0,n):
                        V[k][j] = copy(V[k][j-inc])
                    j -= inc
                    if (j < inc):
                        break
                W[j] = copy(sw)
                for k in xrange(0,m):
                    U[k][i] = copy(su[k])
                for k in xrange(0,n):
                    V[k][i] = copy(sv[k])
            condition = (inc > 1)
        # end do-while #2
        
        # ***** Flip signs *****
        for k in xrange(0,n):
            s = 0
            for i in xrange(0,m):
                if(U[i][k] < 0.0):
                    s += 1
            for j in xrange(0,n):
                if(V[j][k] < 0.0):
                    s += 1
            if (s > (m+n)/2):
                for i in xrange(0,m):
                    U[i][k] = -U[i][k]
                for j in xrange(0,n):
                    V[j][k] = -V[j][k]
        # end reorder            
        
        
    def dist(self,a,b):
        return math.sqrt(pow(float(a),2) + pow(float(b),2))
    
    def SIGN(self,a,b):
        return (a if a>=0 else -a) if b>=0 else (-a if a>=0 else a)
    
    
    