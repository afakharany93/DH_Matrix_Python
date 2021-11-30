#!/usr/bin/env python
# coding: utf-8

from dh import dh_solver
#from IPython.display import Latex 
import sympy
from sympy import Symbol
import numpy as np



#create an object 
mtb = dh_solver()


# ## adding the dh paramters
# just use obj.add() method to add a set of dh paramters in the kinematic chain, the first one to add is the base and the last one is the end effector, the method takes input a list \[ d, theta, a, alpha\]
# 
# you can get the parameters from vrep http://www.forum.coppeliarobotics.com/viewtopic.php?f=9&t=5367

# In[3]:


#you can add the paramters wiht the variable as string
mtb.add([0,Symbol("theta1"),0.467,0])
#or you can add the variable as a Sympy symbol, in this case you can also shift the variable
mtb.add([0,Symbol("theta2")+sympy.pi/2,0.4005,0])
mtb.add([0.2,sympy.pi/3,0,Symbol("alpha3")])


#to get the dh matrices in symbolic form
T = mtb.calc_symbolic_matrices()
print(T)
#simplifing T
sympy.simplify(T)

#to get the intermediate the transormation matrices
print(mtb.T_list)


#to get the matrix with the constants substituted
T1 = mtb.calc_dh_matrix()


T2 = sympy.simplify(T1)
print(T2)


#printing T2 in latex 
# a = sympy.latex(T2)
# print(a)

#to substitute with the variables and return a numpy array of floats, all variables must be subistituted
arr = mtb.get_numpy_matrix([ ["theta1", sympy.pi/2], ["theta2", sympy.pi/3] ,["alpha3", 0.5]])

print(arr)

# to call obj.get_numpy_matrix() you have to at least have called obj.calc_dh_matrix() and of coarse added your parameters :D


