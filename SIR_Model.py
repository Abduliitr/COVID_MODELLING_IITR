## IMPLEMENTING SIR MODEL

# importing required libraries
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import preprocessing
import time
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')
import os
from scipy import integrate, optimize


# defining directories for saving output.
script_dir = os.path.dirname(__file__)
results_dir = os.path.join(script_dir, 'SIR-MODEL-Output/')

if not os.path.isdir(results_dir):
    os.makedirs(results_dir)

## reading datasets
submission_example = pd.read_csv("./covid19-global-forecasting-week-2/submission.csv")
test = pd.read_csv("./covid19-global-forecasting-week-2/test.csv")
train = pd.read_csv("./covid19-global-forecasting-week-2/train.csv")

# Susceptible equation
def fa(N, a, b, beta):
    fa = -beta*a*b
    return fa

# Infected equation
def fb(N, a, b, beta, gamma):
    fb = beta*a*b - gamma*b
    return fb

# Recovered/deceased equation
def fc(N, b, gamma):
    fc = gamma*b
    return fc

# Runge-Kutta method of 4rth order for 3 dimensions (susceptible a, infected b and recovered r)
def rK4(N, a, b, c, fa, fb, fc, beta, gamma, hs):
    a1 = fa(N, a, b, beta)*hs
    b1 = fb(N, a, b, beta, gamma)*hs
    c1 = fc(N, b, gamma)*hs
    ak = a + a1*0.5
    bk = b + b1*0.5
    ck = c + c1*0.5
    a2 = fa(N, ak, bk, beta)*hs
    b2 = fb(N, ak, bk, beta, gamma)*hs
    c2 = fc(N, bk, gamma)*hs
    ak = a + a2*0.5
    bk = b + b2*0.5
    ck = c + c2*0.5
    a3 = fa(N, ak, bk, beta)*hs
    b3 = fb(N, ak, bk, beta, gamma)*hs
    c3 = fc(N, bk, gamma)*hs
    ak = a + a3
    bk = b + b3
    ck = c + c3
    a4 = fa(N, ak, bk, beta)*hs
    b4 = fb(N, ak, bk, beta, gamma)*hs
    c4 = fc(N, bk, gamma)*hs
    a = a + (a1 + 2*(a2 + a3) + a4)/6
    b = b + (b1 + 2*(b2 + b3) + b4)/6
    c = c + (c1 + 2*(c2 + c3) + c4)/6
    return a, b, c

def SIR(N, b0, beta, gamma, hs):
    
    """
    N = total number of population
    beta = transition rate S->I
    gamma = transition rate I->R
    k =  denotes the constant degree distribution of the network (average value for networks in which 
    the probability of finding a node with a different connectivity decays exponentially fast
    hs = jump step of the numerical integration
    """
    
    # Initial condition
    a = float(N-1)/N -b0
    b = float(1)/N +b0
    c = 0.

    sus, inf, rec= [],[],[]
    for i in range(10000): # Run for a certain number of time-steps
        sus.append(a)
        inf.append(b)
        rec.append(c)
        a,b,c = rK4(N, a, b, c, fa, fb, fc, beta, gamma, hs)

    return sus, inf, rec

## IDEAL SIR model
# Parameters of the model
N = 7800*(10**6)
b0 = 0
beta = 0.7
gamma = 0.2
hs = 0.1

sus, inf, rec = SIR(N, b0, beta, gamma, hs)

f = plt.figure(figsize=(8,5)) 
plt.plot(sus, 'b.', label='susceptible')
plt.plot(inf, 'r.', label='infected')
plt.plot(rec, 'c.', label='recovered/deceased')
plt.title("SIR model")
plt.xlabel("time", fontsize=10)
plt.ylabel("Fraction of population", fontsize=10)
plt.legend(loc='best')
plt.xlim(0,1000)

# saving the file
sample_file_name = "SIR_Example.png"
plt.savefig(results_dir + sample_file_name)
# plt.show()
f.clear()

## Fitting SIR parameters to Real Data (Italy)
pop_italy = 60486683.
confirmed_total_date_Italy = train[train['Country_Region']=='Italy'].groupby(['Date']).agg({'ConfirmedCases':['sum']})
fatalities_total_date_Italy = train[train['Country_Region']=='Italy'].groupby(['Date']).agg({'Fatalities':['sum']})
total_date_Italy = confirmed_total_date_Italy.join(fatalities_total_date_Italy)
population = float(pop_italy)
country_df = total_date_Italy[9:]
country_df['day_count'] = list(range(1,len(country_df)+1))

ydata = [i for i in country_df.ConfirmedCases['sum'].values]
xdata = country_df.day_count
ydata = np.array(ydata, dtype=float)
xdata = np.array(xdata, dtype=float)

N = population
inf0 = ydata[0]
sus0 = N - inf0
rec0 = 0.0

def sir_model(y, x, beta, gamma):
    sus = -beta * y[0] * y[1] / N
    rec = gamma * y[1]
    inf = -(sus + rec)
    return sus, inf, rec

def fit_odeint(x, beta, gamma):
    return integrate.odeint(sir_model, (sus0, inf0, rec0), x, args=(beta, gamma))[:,1]

popt, pcov = optimize.curve_fit(fit_odeint, xdata, ydata)
fitted = fit_odeint(xdata, *popt)

f = plt.figure(figsize=(8,5)) 
plt.plot(xdata, ydata, 'o', label="predicted")
plt.plot(xdata, fitted , label="Actual")
plt.title("Fit of SIR model to Italy infected cases")
plt.ylabel("Population infected")
plt.xlabel("Days")
plt.xlim(0, 100)
# plt.show()

print("For Fit of SIR model to Italy infected cases :")
print("Optimal parameters: beta =", popt[0], " and gamma = ", popt[1])
print("-------------------------------------------------------------")

# saving the file
sample_file_name = "SIR_Italy.png"
plt.savefig(results_dir + sample_file_name)
# plt.show()
f.clear()

## Fitting SIR parameters to Real Data (India)
pop_india = 1380004385.
confirmed_total_date_India = train[train['Country_Region']=='India'].groupby(['Date']).agg({'ConfirmedCases':['sum']})
fatalities_total_date_India = train[train['Country_Region']=='India'].groupby(['Date']).agg({'Fatalities':['sum']})
total_date_India = confirmed_total_date_India.join(fatalities_total_date_India)
population = float(pop_india)
country_df = total_date_India[9:]
country_df['day_count'] = list(range(1,len(country_df)+1))

ydata = [i for i in country_df.ConfirmedCases['sum'].values]
xdata = country_df.day_count
ydata = np.array(ydata, dtype=float)
xdata = np.array(xdata, dtype=float)

N = population
inf0 = ydata[0]
sus0 = N - inf0
rec0 = 0.0

popt, pcov = optimize.curve_fit(fit_odeint, xdata, ydata)
fitted = fit_odeint(xdata, *popt)

plt.plot(xdata, ydata, 'o')
plt.plot(xdata, fitted)
plt.title("Fit of SIR model to India infected cases")
plt.ylabel("Population infected")
plt.xlabel("Days")
# plt.ylim(0, 20000)
plt.xlim(0, 100)
# plt.show()
print("For Fit of SIR model to India infected cases :")
print("Optimal parameters: beta =", popt[0], " and gamma = ", popt[1])
print("-------------------------------------------------------------")

# saving the file
sample_file_name = "SIR_India.png"
plt.savefig(results_dir + sample_file_name)
# plt.show()
