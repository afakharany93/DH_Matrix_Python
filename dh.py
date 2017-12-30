from sympy import *
import numpy as np
from tqdm import tqdm

class dh_solver():
    def __init__(self):
        self.joints_list = []
        self.T_list = []
        self.T = eye(4)
        self.T_sub = eye(4)
    
    def add(self,dh_param):
        if len(dh_param)!=4:
            raise ValueError('the number of input dh parameters !=4, it should be structure as [d,theta,a, alpha].')
        else:
            self.joints_list.append(dh_param)
            
    def dh_matrix(self,parameters):
        d,theta,a, alpha = parameters
        #first row
        dh11 = cos(theta)
        dh12 =  -1*sin(theta)*cos(alpha)
        dh13 = sin(theta)*sin(alpha)
        dh14 =  a*cos(theta)
        #second row
        dh21 = sin(theta)
        dh22 = cos(theta)*cos(alpha)
        dh23 = -1*cos(theta)*sin(alpha)
        dh24 = a*sin(alpha)
        #third row
        dh31 =  0
        dh32 =  sin(alpha)
        dh33 =  cos(alpha)
        dh34 =  d
        #forth row
        dh41 = 0
        dh42 = 0
        dh43 = 0
        dh44 = 1    
        return Matrix([[dh11, dh12, dh13, dh14],
                     [dh21, dh22, dh23, dh24],
                     [dh31, dh32, dh33, dh34],
                     [dh41, dh42, dh43, dh44]])

    def calc_symbolic_matrices(self):
        self.T_list = []
        self.T = eye(4)
        for i in tqdm(range(len(self.joints_list))):
            d = Symbol("d"+str(i+1))
            theta = Symbol("theta"+str(i+1))
            a = Symbol("a"+str(i+1))
            alpha = Symbol("alpha"+str(i+1))
            parameters = [d,theta,a,alpha]
            Tn = self.dh_matrix(parameters)
            self.T_list.append(Tn)
            self.T=self.T*Tn
        return self.T

    def calc_dh_matrix(self):
        self.calc_symbolic_matrices()
        self.T_sub = self.T
        for i in tqdm(range(len(self.joints_list))):
            ds = "d"+str(i+1)
            thetas = "theta"+str(i+1)
            a_s = "a"+str(i+1)
            alphas = "alpha"+str(i+1)
            parameters = [ds,thetas,a_s,alphas]
            for pair in zip(parameters,self.joints_list[i]):
#                 print(pair)
                self.T_sub = self.T_sub.subs(pair[0], pair[1])
        return self.T_sub
    
    def get_numpy_matrix(self, list_subs):
#         self.calc_dh_matrix()
        T = (self.T_sub.subs(list_subs)).evalf()
        return np.array(T.tolist()).astype(np.float64)

