import numpy as np

t0=0
x = 3
t1=0
tx = [t0,t1]
tx = np.array(tx).reshape(2,1)
z = pow(10,-4)

a = np.array([[1, 2], [3, 4]])
mu = np.mean(a,axis=0)

print(a,"\n",mu,"\n",np.subtract(a,mu))



#print(tx)
#print(z)
#print(j_hist)
#print (theta[1])
#print (tx[x])
#print(a)
#print(np.square(a)) # Element wise square of matrix a
#print(np.power(a,2))# Prints the element wise power of N
#print(a[:,0:2])     # Prints the first two columns
#print(a[0:2,:])     # Prints the first two rows