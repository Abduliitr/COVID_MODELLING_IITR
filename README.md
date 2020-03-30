# COVID_MODELLING_IITR

## Team Members
1. Abdulahad Khan 17112002
2. Abhishek Kumar 17112005
3. Ayush Kumar 17112011
4. Shuvam Samadder 17112076

## Libraries
Make sure to import the following libraries in your machine to initiate.

```bash
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import preprocessing
import time
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')
import scipy as sp
import os
from scipy import integrate, optimize
```
## Basic Analysis Secttion

First of all, let's take a look at some elementary data analysis of our dataset.

### Global Trend

The following plot perfectly depicts the confirmed global confirmed and death trend in a time series manner.

![Global Case Trend](https://raw.githubusercontent.com/Abduliitr/COVID_MODELLING_IITR/master/Basic-Analysis-Output/Global_trend.png?token=AO7DFZWNXANY63HR5CGR33C6QH53G)

### China Trend

China was the first country to be infected from the virus. Due to this they were not prepared for the virus even they failed to identify the virus until they had suffciently high number of confirmed cases. That's why initially china had a quite high mortality rate initially but due to some strict contanment meeasures they were succesful to contain the spread of the virus inside their country.

![China Case Trend](https://raw.githubusercontent.com/Abduliitr/COVID_MODELLING_IITR/master/Basic-Analysis-Output/China_trend.png?token=AO7DFZRHQGI5E3QVO2BEEJS6QH7YQ)

### India Trend

As per a estimate China had it's first case in December 2019 but India got it's first case pretty late i.e. around 31st January 2020. The following trend depicts the 

![China Case Trend](https://raw.githubusercontent.com/Abduliitr/COVID_MODELLING_IITR/master/Basic-Analysis-Output/India_trend.png?token=AO7DFZUFEUBMDJK2WOJO5JC6QIARI)

### Italy, Spain, UK and India

Italy and Spain are the most affected countries in the Europian Union. Athough UK was a integral part of Europian union before the Brexit but after that the connectivity between Europe and UK became weak which helped to mitigate the initial import related spread of corona virus in UK from the rest of the Europian Union countries.

![Italy, Spain, UK and India Case Trend](https://raw.githubusercontent.com/Abduliitr/COVID_MODELLING_IITR/master/Basic-Analysis-Output/India_%26_3_others_trend.png?token=AO7DFZVXHZL2IMBUSAWGYBC6QIBUU)








