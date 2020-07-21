import pandas as pd

#importing the data
df_cap = pd.read_csv(r'C:\Users\User\Documents\Projects\Health Expenditure OECD\cap.csv', index_col = 'Country')
df_pop = pd.read_csv(r'C:\Users\User\Documents\Projects\Health Expenditure OECD\israel pop.csv')
df_budget = pd.read_csv(r'C:\Users\User\Documents\Projects\Health Expenditure OECD\budgets.csv')
df_oecd = pd.read_csv(r'C:\Users\User\Documents\Projects\Health Expenditure OECD\OECD pop.csv')

#pivoting the data
df_pop = df_pop.pivot(index = 'Year', columns = 'Age', values = 'Population')
df_budget = df_budget.pivot(index = 'Year', columns = 'Country', values = 'Value')
df_oecd = df_oecd.pivot(index = 'Year', columns = 'Country', values = 'Value')

#creating a new DataFrame to work with for the Israeli population
df_i_new_pop = pd.DataFrame(columns = df_cap.columns)

#inserrting manualy the first and last columns
df_i_new_pop['0_4'] = df_pop['0_4']
df_i_new_pop['85_OVER'] = df_pop['85_OVER']

#filling the rest of the columns by combining two 5 year brackets into 10 year brackets
c = 1
for i in df_i_new_pop.columns[1:-1]:
    df_i_new_pop[i] = df_pop.iloc[:, c] + df_pop.iloc[:, c+1]
    c += 2

#creating a new DataFrame to work with for the OECD reference
df_r_oecd = pd.DataFrame(index = df_i_new_pop.index, columns = df_cap.columns)
  
"""filling the DataFrame by dividing each age group of the Israeli population
 by the total population to get the ratio for that group"""
for i in df_r_oecd.index:
    df_r_oecd.loc[i,:] = df_i_new_pop.loc[i,:]/df_i_new_pop.loc[i,:].sum(axis = 0)

#creating two DataFrames to work with, one temporary and the second for the results
df_temp = pd.DataFrame(index = df_r_oecd.index, columns = df_cap.columns) 
df_results = pd.DataFrame(index = df_r_oecd.index, columns = df_oecd.columns)

"""a loop to fill a DataFrame, first it calculate the effective population in a country,
 and the it calcualte the country's budget according to that population"""
for country in df_budget.columns:
    for year in df_r_oecd.index:
        df_temp.loc[year, :] = df_r_oecd.loc[year, :] * df_oecd.loc[year, country]
        df_temp.loc[year, :] *= df_cap.loc[country, :]
        df_results.loc[year, country] = df_budget.loc[year, country] / df_temp.loc[year,:].sum(axis = 0) * 1000000
 
#exporting the data to a csv file       
df_results.to_csv(r'C:\Users\User\Documents\Projects\Health Expenditure OECD\results.csv')
