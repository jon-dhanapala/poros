import pandas as pd
import scipy.stats
import numpy as np

KTEST_CDFS = [
    "norm",            #Normal (Gaussian)
    "alpha",           #Alpha
    "anglit",          #Anglit
    "arcsine",         #Arcsine
    "beta",            #Beta
    "betaprime",       #Beta Prime
    "bradford",        #Bradford
    "burr",            #Burr
    "cauchy",          #Cauchy
    "chi",             #Chi
    "chi2",            #Chi-squared
    "cosine",          #Cosine
    "dgamma",          #Double Gamma
    "dweibull",        #Double Weibull
    "erlang",          #Erlang
    "expon",           #Exponential
    "exponweib",       #Exponentiated Weibull
    "exponpow",        #Exponential Power
    "fatiguelife",     #Fatigue Life (Birnbaum-Sanders)
    "foldcauchy",      #Folded Cauchy
    "f",               #F (Snecdor F)
    "fisk",            #Fisk
    "foldnorm",        #Folded Normal
    "frechet_r",       #Frechet Right Sided, Extreme Value Type II
    "frechet_l",       #Frechet Left Sided, Weibull_max
    "gamma",           #Gamma
    "gausshyper",      #Gauss Hypergeometric
    "genexpon",        #Generalized Exponential
    "genextreme",      #Generalized Extreme Value
    "gengamma",        #Generalized gamma
    "genlogistic",     #Generalized Logistic
    "genpareto",       #Generalized Pareto
    "genhalflogistic", #Generalized Half Logistic
    "gilbrat",         #Gilbrat
    "gompertz",        #Gompertz (Truncated Gumbel)
    "gumbel_l",        #Left Sided Gumbel, etc.
    "gumbel_r",        #Right Sided Gumbel
    "halfcauchy",      #Half Cauchy
    "halflogistic",    #Half Logistic
    "halfnorm",        #Half Normal
    "hypsecant",       #Hyperbolic Secant
    "invgamma",        #Inverse Gamma
    "invnorm",         #Inverse Normal
    "invweibull",      #Inverse Weibull
    "johnsonsb",       #Johnson SB
    "johnsonsu",       #Johnson SU
    "laplace",         #Laplace
    "logistic",        #Logistic
    "loggamma",        #Log-Gamma
    "loglaplace",      #Log-Laplace (Log Double Exponential)
    "lognorm",         #Log-Normal
    "lomax",           #Lomax (Pareto of the second kind)
    "maxwell",         #Maxwell
    "mielke",          #Mielke's Beta-Kappa
    "nakagami",        #Nakagami
    "ncx2",            #Non-central chi-squared
    "ncf",             #Non-central F
    "nct",
    "poisson"            #Non-central Student's T
    "pareto",          #Pareto
    "powerlaw",        #Power-function
    "powerlognorm",    #Power log normal
    "powernorm",       #Power normal
    "rdist",           #R distribution
    "reciprocal",      #Reciprocal
    "rayleigh",        #Rayleigh
    "rice",            #Rice
    "recipinvgauss",   #Reciprocal Inverse Gaussian
    "semicircular",    #Semicircular
    "t",               #Student's T
    "triang",          #Triangular
    "truncexpon",      #Truncated Exponential
    "truncnorm",       #Truncated Normal
    "tukeylambda",     #Tukey-Lambda
    "uniform",         #Uniform
    "vonmises",        #Von-Mises (Circular)
    "wald",            #Wald
    "weibull_min",     #Minimum Weibull (see Frechet)
    "weibull_max",     #Maximum Weibull (see Frechet)
    "wrapcauchy",      #Wrapped Cauchy
    "ksone",           #Kolmogorov-Smirnov one-sided (no stats)
    "kstwobign"        #Kolmogorov-Smirnov two-sided test for Large N
    ]

def read_data(file_name):
    iat = pd.read_csv(file_name)
    return iat

def kstest_distribution(file_name,col_name):
    sample = read_data(file_name)[col_name]
    for cdf in KTEST_CDFS:
        try:
            #fit our data set against every probability distribution
            parameters = eval("scipy.stats."+cdf+".fit(sample)");
            #Applying the Kolmogorov-Smirnof one sided test
            D, p = scipy.stats.kstest(sample, cdf, args=parameters);
            #pretty-print the results
            print(cdf.ljust(16) + (",p: ,"+str(p)).ljust(25)+",D: ,"+str(D))
        except:
            c = 2

def chi_squared_test(file_name,col_name):

    data = read_data(file_name)[col_name].values

    test = np.random.poisson(data.mean(), len(data))
    chisq, p_value = scipy.stats.chisquare(test,data)
    print("poisson, " + ",chi, "+str(chisq)  + ",p_value, "+str(p_value))

    test = np.random.normal(data.mean(), len(data))
    chisq, p_value = scipy.stats.chisquare(test,data)
    print("normal, "+" ,chi, "+str(chisq)+" ,p_value, "+str(p_value))

    test = np.random.gamma(data.mean(), len(data))
    chisq, p_value = scipy.stats.chisquare(test,data)
    print("gamma, "+" ,chi, "+str(chisq)+" ,p_value, "+str(p_value))

    test = np.random.exponential(data.mean(), len(data))
    chisq, p_value = scipy.stats.chisquare(test,data)
    print("exponential, "+" ,chi, "+str(chisq)+" ,p_value, "+str(p_value))

    test = np.random.lognormal(data.mean(), len(data))
    chisq, p_value = scipy.stats.chisquare(test,data)
    print("lognormal, "+" ,chi, "+str(chisq)+" ,p_value, "+str(p_value))

    test = np.random.weibull(data.mean(), len(data))
    chisq, p_value = scipy.stats.chisquare(test,data)
    print("weibull, "+" ,chi, "+str(chisq)+" ,p_value, "+str(p_value))

    test = np.random.beta(data.mean(), len(data))
    chisq, p_value = scipy.stats.chisquare(test,data)
    print("beta, "+" ,chi, "+str(chisq)+" ,p_value, "+str(p_value))

def main():
    print("k_test_interarrival_times")
    kstest_distribution('interarrival_times.csv','inter_arrival_time')
    print()
    print()
    print("k_test_service_times")
    kstest_distribution('service_times.csv','service_times')
    print("chi_test_interarrival_times")
    chi_squared_test('interarrival_times.csv','inter_arrival_time')
    print()
    print()
    print("chi_test_service_times")
    chi_squared_test('service_times.csv','service_times')

if __name__ == '__main__':
    main()
