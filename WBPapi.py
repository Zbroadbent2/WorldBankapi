#%%
import wbgapi as wdi #World Bank API package 

import seaborn as sns
import seaborn.objects as so
import matplotlib.pyplot as plt 

import pandas as pd
import numpy as np

import statsmodels.api as sm
import statsmodels.formula.api as smf
#%%

# QUESTION 1 - Choose 3 variables at the continuous level of measurement
#Continuous meaning income, years, percentages rates
#I will be going with GDP per capita (income)
#Life expectancy (years)
#Urban population percentage (%)

#Each string is a World Bank indicator code, storing codes in memory
series_list = [
    "NY.GDP.PCAP.CD", # GDP per capita — continuous money variable
    "SP.DYN.LE00.IN", # Life expectancy — continuous
    "SP.URB.TOTL.IN.ZS" # Urban population — continuous percentage
]
#%%
year = 2019
#%%
#Downloading the data

df = wdi.data.DataFrame( #This line tells the API to give data and return it as a pandas DF
    series=series_list, #Download the 3 variables we stored earlier
    economy="all", #Give me all countries 
    time=year, #Give me only 2019
    numericTimeKeys=True,
    columns="series" #Make each variable its own column
).reset_index() #API returns a structured format. Converts it into a normal table

df.head() #Shows the first 5 rows so I can see if it works
#%%
#Clean variable names 
df  = df.rename(columns={
    "NY.GDP.PCAP.CD": "GDPpc",
    "SP.DYN.LE00.IN": "Life",
    "SP.URB.TOTL.IN.ZS": "UrbanPct"
    })
df.head()
#%%
#QUESTION 2 - Visulaize the relationship between one
#indepenedent variable and the dependent variable

plt.figure(figsize=(8,5)) #Creates the graph window and sets size

sns.scatterplot(data=df, x="Life", y="GDPpc") #Creates scatterplot, each dot = 1 country

#Titles and labels
plt.title("Life Expectancy vs GDP per Capita (2019)")
plt.xlabel("Life Expectancy (Years)")
plt.ylabel("GDP per Capita (Current US$)")

plt.show() #Graph display
#After running, I observe that most countries life expectancy is typically around 60-80
#I also see that GDP per capita increases as life expectancy increases
#%%
#Cleaning the data, no missing values, complete observations
#Listwise deletion
df_clean = df.dropna(subset=["GDPpc", "Life", "UrbanPct"])

df_clean.shape
#%%
#QUESTION 3 - Use statsmodels to estimate a multiple regression model
#and estimate one slop coefficient and one model statistic


model = smf.ols("GDPpc ~ Life + UrbanPct", data=df_clean).fit() #tells statsmodels to estimate coef.

print(model.summary())

#Slope coefficient for life is 1742.7928. This means:
#A 1-year increase in life expectancy is assciated with an increase of about
#$1,742.79 in GDP per capita, holding UrbanPct constant.
#p-value = 0.000, meaning statistically significant at (p < 0.05)

#R-Squared is 0.38727991450780763, so 0.387.
#This means about 38.7% of the variation in GDP per capita across countries
#is explained by life expectancy and urban population percentage.
#Other factors may also affect GDP (education, institutions, trade, etc.)