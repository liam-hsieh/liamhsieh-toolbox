# toolbox.stats.GammaLinearCombination
*class* 

## toolbox.stats.GammaLinearCombination.pdf
*method* return probability density

## toolbox.stats.GammaLinearCombination.cdf
*method* return cumulative probability

## toolbox.stats.GammaLinearCombination.plot_pdf
*method* plot graph of pdf

## toolbox.stats.GammaLinearCombination.percentile
*method* return percentage value

## toolbox.stats.GammaLinearCombination.rv
*method* generate random variable(s)


# Behind this module
This module create pdf/cdf/percentile for the linear combination of gamma distributed variables.


For example, end-to-end cycle time of a particular product in a wafer fab is composed by hundreds of time segments, e.g., equipment processing time or transportation time, and they are assumed as independent gamma distributed variables. Let $x_i$ be the time segment $i$ which follows gamma distribution: $x_i \overset{\mathrm{i.i.d.}}\sim \Gamma(\alpha_i, \beta_i)$ for $i=1,2,\ldots,n$ and the density function is given by


$$
f_i(x_i)=
\begin{cases}
 \frac{x_i^{\alpha_i-1}e^{-\frac{x_i}{\beta_i}}}{\beta_i^{\alpha_i}\Gamma(\alpha_i)}&, \forall x_i>0\\
 0 &  \text{, otherwise}
 \end{cases}
$$

The linear combination of $x_i$, say $y$, is defined by $\sum_{i=1}^n c_i x_i$ where $c_i \in \mathbf{R_+}$. 

Mathai, A. M. [^Mathai1982] provided a finite sum as density of $y$ in terms of zonal polynomials and confluent hypergeometric functions. Moschopoulos, P. G. [^Moschopoulos1985] proposed different way to deal with it which can express the density by single gamma-series whose coefficients are computed by simple recursive relations. Because the ease of implementation, this module is based on Moschopoulos's approach.


Since the $x_i$'s are independent, the moment generating function (MGF) of $y$ is the product of the MGF's of the $x_i$'s, i.e., 

$$
M(t) = \prod_{i=1}^n(1-\beta_i t)^{-\alpha_i}
$$

Let $\beta_1$ be the $\min(\beta_i)$; application of the identity 

$$
1-\beta_i t = \frac{(1-\beta_1 t)\beta_i}{\beta_1}(1-\frac{1-\beta_1/\beta_i}{1-\beta_1 t})
$$

to the MGF gives,

$$
\log M(t)=\log[C(1-\beta_1 t)^{-\rho}] + \sum_{k=1}^\infty \gamma_k(1-\beta_1 t)^{-k}
$$

where

$$
C = \prod_{i=1}^n(\beta_1/\beta_i)^{\alpha_i}
$$

,

$$
\gamma_k = \sum_{i=1}^n \frac{\alpha_i (1-\beta_1/\beta_i)^k}{k}, \quad k=1,2,\ldots, \infty
$$

, and 

$$
\rho = \sum_{i=1}^n \alpha_i>0 .
$$

The expression is valid for all $t$ such that $\max\limits_{i}|\frac{(1-\beta_1/\beta_i)}{1-\beta_1 t}|<1$.
Thus, $M(t)$ can be expressed as 

$$
M(t) = C(1-\beta_1 t)^{-\rho} e^{\sum_{k=1}^\infty \gamma_k(1-\beta_1 t)^{-k}}
$$

Let

$$
e^{\sum_{k=1}^\infty \gamma_k(1-\beta_1 t)^{-k}} = \sum_{k=0}^{\infty} \delta_k(1-\beta_1 t)^{-k}
$$

, then upon differentiating with respect to $(1-\beta_1 t)^{-1}$ follows that the coefficients $\delta_k$ can be obtained by the recursive function:

$$
\delta_{k+1} = \frac{1}{k+1}\sum^{k+1}_{i=1} i \gamma_i \delta_{k+1-i}, \quad k=0,1,\ldots, \infty
$$

with $\delta_0 = 1$.
Therefore, we can now obtain a gamma-series representation for the density of $y$.

The distribution of $y$ is shown as follows:

$$
f(y) = C \sum_{k=0}^{\infty}\frac{\delta_k y^{\rho + k -1}e^{-\frac{y}{\beta_1}}}{\Gamma(\rho + k) \beta_1^{\rho+k}}, \quad y>0
$$

where

$$
C = \prod_{i \in N}(\frac{\beta_l}{\beta_i})^{\alpha_i},
$$

$$
\rho = \sum_{i=1}^{n}\alpha_i \ge 0
$$

$$
\delta_k = \frac{1}{k} \sum^{k}_{i=1} i \gamma_i \delta_{k-i}, \quad k=1,2, \ldots, \infty
$$ 

with $\gamma_k = \frac{\sum_{i \in N} \alpha_{i}(1-\frac{\beta_l}{\beta_i})^k}{k}$, and $\delta_0=1$

The uniform convergence of PDF will be:

$$
f(y) = \Bigl(\frac{C\beta_1^{-\rho}}{\Gamma(\rho)}\Bigr)y^{\rho -1} e^{-y(1-b)/\beta_1}
$$

where $b = \max \limits_{2\leq j \leq n}(1-\frac{\beta_1}{\beta_j})$


In practical computation, one may choose the first $k+1$ terms of the series $\delta_{k+1}$ where $k$ is like desired accuracy. A similar case likes Lagrange Error Bound when using Tayler Expansion. In short, the error term caused by a small number of $k$ won't hurt the cycle time approximation significantly.


Since we have PDF approximation for $y$, ideally CDF can also be calculated by for generating random variables:

$$ 
\int_{0}^{y} f(y) dy:=F(y)=Pr(Y\leqq y) = C \sum_{k=0}^{\infty}\delta_k \int_{0}^{y}\frac{y^{\rho+k-1}e^{-\frac{y}{\beta_1}}}{\Gamma(\rho + k)\beta_1^{\rho + k}} dy
$$


Similarly, it is possible to conduct incomplete gamma integral which is common in practice; owing to both lower bound and upper bound estimates of operation cycle time won't be difficult to be obtained, applying numerical method for percentile computation should be acceptable as an easy-to-use solution.


# Appendix
## extend to a linear combination
linear combination can be obtained by the above Gamma sum with scaling.

If $x \sim \text{Gamma}(k,\theta)$ 
then, for any c>0,
$cx \sim \text{Gamma}(k,c\theta)$

or equivalently, 
$cx \sim \text{Gamma}(\alpha, \frac{\beta}{c})$ if $x \sim \text{Gamma}(\alpha,\beta)$ (so-called shape-rate parameterization)


[^Mathai1982]: Mathai, A. M. (1982). "Storage capacity of a dam with gamma type inputs". Annals of the Institute of Statistical Mathematics. 34 (3): 591–597.
[^Moschopoulos1985]: Moschopoulos, P. G. (1985). The distribution of the sum of independent gamma random variables. *Annals of the Institute of Statistical Mathematics*, 37(1), 541-544.