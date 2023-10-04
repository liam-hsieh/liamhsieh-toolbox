import numpy as np
from sklearn.utils.validation import check_array
from regular_sum_distribution import regular_sum_distribution

class GammaLinearCombination:
    regular_sum_distribution = regular_sum_distribution

    def __init__(self, gamma_als: list, const_vector: list = None, accuracy_k: int = 90):
        """initialize by a list of gamma parameter paired lists and approximate distribution for the sum of those gamma distrubted variables
        
        Args:
            gamma_als (List): [
                                [alpha_1, location_1, scale_1],
                                [alpha_2, location_2, scale_2],
                                .
                                . 
                                [alpha_n, location_n, scale_n],
                             ]
                             include n paired lists for parameter alpha and location and scale
            const_vector (List): constants vectors for linear combination
        """
        if isinstance(gamma_als, str): raise ValueError("gamma_als should be a numeric 2D-array")
        gamma_als = check_array(gamma_als,ensure_2d=True)
        self.alpha = gamma_als[:,0]
        self.loc = gamma_als[:,1]
        self.beta = gamma_als[:,2] #here beta refer to the same symbol we use at document, but it equals to parameter scale in scipy.gamma document
        self.accuracy_k = accuracy_k
        self.N = []
        self.total_loc = np.nansum(self.loc)


        if const_vector is None:
            self.c = [1] * len(gamma_als)
        else:
            self.c = const_vector

    # def sum_type_determine(gamma_als):
    #     segments_status = [
    #         [1,0,0] if np.isnan(s).sum==0 else [0,1,0] if np.isnan(s).sum==2 else [0,0,1] for s in gamma_als
    #     ]
    #     eff_segments = gamma_als[np.where(segments_status[:,0]==1)] #self.N
    #     sum_type =""
    #     return sum_type

    def _pdf(self, x):
        return x
    def _cdf(self, x):
        return x
    def _ppf(self, x):
        return x    

    def ppf(self, p: float) -> float:
        """return percentage value at given percentage

        Args:
            p (float): percentage; 0<p<1

        Returns:
            float: percentage value
        """
        return self._ppf(p)
    
    def cdf(self,x: float) -> float:
        """return cumulative probability

        Args:
            x (float): value

        Returns:
            float: probability
        """
        return self._cdf(x)
        
    def pdf(self,x: float) -> float:
        """return probability density

        Args:
            x (float): value

        Returns:
            float: probability
        """
        return self._pdf(x)

    def rv(self, num: int =1) -> list:
        """generate random variable(s)

        Args:
            num (int, optional): number of random variables. Defaults to 1.

        Returns:
            List: a list of generated random variables
        """
        rvs = None
        return rvs

    # def plot_pdf(self):
    #     return ANY_FIGURE_INSTANCE_FOR_PDF