import numpy as np

a = range(16)
a = np.reshape(a,(4,4))
theta = np.zeros((2, 1), dtype=int)
t0=0
x = 3
t1=0
tx = [t0,t1]
print(tx)
tx = np.array(tx).reshape(2,1)
z = pow(10,-4)
print(z)


#print(j_hist)
#print (theta[1])
#print (tx[x])
#print(a)
#print(np.square(a)) # Element wise square of matrix a
#print(np.power(a,2))# Prints the element wise power of N
#print(a[:,0:2])     # Prints the first two columns
#print(a[0:2,:])     # Prints the first two rows