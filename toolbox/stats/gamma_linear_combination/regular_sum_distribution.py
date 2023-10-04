from statistics import mode
import random
import math

class SumDistribution:
    __slots__ = [
        'total_loc',
        
    ]

    def __init__(self):
        self.total_loc = None
        self.N = None #number of segments
        self.alpha = None
        self.beta = None
        self.loc = None
        self.beta_min = None
        self.k_max
        self.pdf


    def get_y_Ubound(self):
        """find maximum of f

        Args:
            x_init (_type_): _description_
            f (_type_): _description_
        """
        f = self.pdf
        Prob_tol = 0
        x_start = self.total_loc
        step_size =  self.total_loc/1000 #0.05

        x = x_start
        while f(x)<f(x+step_size):
            x = x + step_size
        Prob_tol = f(x) - f(x+step_size)
        step_size = self.total_loc/10000

        while f(x)<f(x + step_size):
            x = x + step_size

        mode = x
        return  f(x) + Prob_tol #yUbound

    def gen_sample_by_sum_pdf(self):
        '''
        bound it appropriately to apply acceptance-reject algorithm
        '''

        xbounds = [self.total_loc, xUbound]
        ybounds = [0, yUbound]
        i = 0
        x_samples = []
        y_samples = []

        while i<10000:
            x_draw = random.uniform(xbounds[0], xbounds[1])
            y_draw = self.pdf(x_draw)
            if y_draw >= random.uniform(ybounds[0], ybounds[1]):
                x_samples.append(x_draw)
                y_samples.append(y_draw)
                i = i + 1
        return sorted(x_samples, reverse  =True), sorted(y_samples, reverse = True)

    def create_gamma_k(self):
        gamma_k = []
        for k in range(self.k_max + 1):
            if k==0:
                gamma_k.append(1)
            else:
                gamma_k.append(
                    sum([self.alpha[i]*(1-(self.beta_min/self.beta[i]))**k for i in self.N]) / k 
                )

        self.gamma_k = gamma_k

    def _sum_pdf(self, x):
        x = x - self.total_loc
        if x>0:
            prob = self.C * sum([self.delta_k[k] * (x**(self.rho + k - 1)) * math.exp(-x/self.beta_min)/(math.gamma(self.rho + k) * (self.beta_min**(self.rho + k))) for k in range(0, self.k_max)])
        else:
            prob = 0
        return prob

    def regular_sum_distribution(gamma_als):


        return None