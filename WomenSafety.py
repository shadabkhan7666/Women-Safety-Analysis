import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 


df = pd.read_csv("CrimesOnWomenData.csv") 
print(df) 


# check first 5 rows 
print("\n--- First 5 Rows ---")
print(df.head(5)) 

# check last 5 rows 
print("\n--- Last 5 Rows ---") 
print(df.tail(5)) 

# information about dataframe 
print("\n--- DataFrame Info ---")
print(df.info()) 

# stastical summary of the dataframe 
print("\n--- Statistical Summary ---")
print(df.describe()) 

# check data types 
print("\n--- Data Types ---")
print(df.dtypes) 

# check duplicate records 
duplicate_checking = df.duplicated().sum() 
print(f"\nTotal Duplicates: {duplicate_checking}") 

# check null values 
null_checking = df.isnull().sum() 
print("\n--- Null Values ---")
print(null_checking) 

# Check for extra spaces in state names
extra_space = df[(df["State"]) != (df["State"].str.strip())] 
print("\n--- States with extra spaces ---")
print(extra_space) 

# finding a correlation 
# correlation tells strength so in this calculation it tells weak correlation 
correlation = df["Year"].corr(df["Rape"]) 
print(f"\nCorrelation between Year and Rape: {correlation}")

# finding a covariance 
# covariance tells perfect relation both are increased  
covariance = df["Year"].cov(df["Rape"]) 
print(f"Covariance between Year and Rape: {covariance}") 

# Check for invalid values (negative numbers)
invalidvalue = df[(df["Year"] < 0) | (df["Rape"] < 0) | (df["K&A"]< 0) | 
               (df["DD"] < 0) | (df["AoW"] < 0)| (df["AoM"] < 0) | 
                (df["DV"] < 0) | (df["WT"] < 0)] 
print("\n--- Invalid Values (Negative) ---")
print(invalidvalue) 

# state names 
state_name = df["State"].unique() 
print("\n--- State Names ---")
print(state_name) 

# Total states 
total_states = df["State"].nunique() 
print(f"\nTotal States: {total_states}") 

# min year 
min_year = df["Year"].min() 
print(f"Min Year: {min_year}") 

# max year 
max_year = df["Year"].max() 
print(f"Max Year: {max_year}") 

# checking crime level 
df["Crime_Level"] = np.where( 
    (df["Rape"] > 1000) &  
    (df["K&A"] > 1000) &  
    (df["DD"] > 1000) &  
    (df["AoW"] > 1000) &  
    (df["AoM"] > 1000) &  
    (df["DV"] > 1000) &  
    (df["WT"] > 1000), 
    "High", 
    "Low" 
) 
print("\n--- Data with Crime Level ---")
print(df.head()) 

df["State"] = df["State"].str.strip()
df["State"] = df["State"].str.lower()
df.loc[df["State"] == 'd & n haveli',"State"] = "d&n haveli"

# total crimes with state and year 
summary = pd.pivot_table( 
    df, 
    values = ["Rape","K&A",'DD','AoW','AoM','DV','WT'], 
    index = ['State','Year'], 
    aggfunc = "sum" 
) 
print("\n--- Pivot Table Summary ---")
print(summary.head()) 

# using group by to find top 5 state based on crimes 
grouping = df.groupby("State")[["Rape","K&A",'DD','AoW','AoM','DV','WT']].sum().sort_values(
    by=["Rape","K&A",'DD','AoW','AoM','DV','WT'],
    ascending=[False,False,False,False,False,False,False]
) 
print("\n--- Grouping by State ---")
print(grouping.head()) 

# checking crime percentage based on state 
melted = df.melt( 
    id_vars=['Year', 'State'], 
    value_vars=['Rape', 'K&A', 'DD', 'AoW', 'AoM', 'DV', 'WT'], 
    var_name='Crime', 
    value_name='Count' 
) 
result = pd.crosstab( 
    melted['State'], 
    melted['Crime'], 
    values=melted['Count'], 
    aggfunc='sum' 
) 

percentage = result.div(result.sum(axis=1), axis=0) * 100 
print("\n--- Crime Percentage by State ---")
print(percentage.head()) 

crime_cols = ['Rape', 'K&A', 'DD', 'AoW', 'AoM', 'DV', 'WT']

df["State"] = df["State"].str.strip()
df["State"] = df["State"].str.lower()


# Data preparation for plots
yearly_rape = df.groupby('Year')['Rape'].sum()
yearly_ka = df.groupby('Year')['K&A'].sum()
state_crimes = df.groupby('State')[crime_cols].sum().head(10)
top10_dv = df.groupby('State')['DV'].sum().sort_values(ascending=False).head(10)
total_crimes = df[crime_cols].sum()
yearly_crimes = df.groupby('Year')[crime_cols].sum()
yearly_total = df.groupby('Year')[crime_cols].sum().sum(axis=1)
state_total = df.groupby('State')[crime_cols].sum().sum(axis=1).sort_values(ascending=False).head(10)


fig1, ax1 = plt.subplots(2, 2, figsize=(15, 12))
fig1.suptitle("Crime Data Analysis - Part 1", fontsize=16)
fig1.subplots_adjust(hspace=0.4) 

# 1. Year-wise Rape Trend
ax1[0, 0].plot(yearly_rape.index, yearly_rape.values, marker='o')
ax1[0, 0].set_title('1. Year-wise Rape Cases')
ax1[0, 0].set_xlabel('Year')
ax1[0, 0].set_ylabel('Rape Cases')

# 2. Year-wise K&A Trend
ax1[0, 1].plot(yearly_ka.index, yearly_ka.values, marker='o', color='orange')
ax1[0, 1].set_title('2. Year-wise K&A Cases')
ax1[0, 1].set_xlabel('Year')
ax1[0, 1].set_ylabel('K&A Cases')

# 3. State-wise crime comparison
state_crimes.plot(kind='bar', stacked=True, ax=ax1[1, 0])
ax1[1, 0].set_title('3. Crime Distribution by State')
ax1[1, 0].set_xlabel('State')
ax1[1, 0].set_ylabel('Total Crimes')
ax1[1, 0].tick_params(axis='x', rotation=45)

# 4. Top 10 States by Domestic Violence
ax1[1, 1].bar(top10_dv.index, top10_dv.values, color='purple')
ax1[1, 1].set_title('4. Top 10 States by Domestic Violence')
ax1[1, 1].set_xlabel('State')
ax1[1, 1].set_ylabel('DV Cases')
ax1[1, 1].tick_params(axis='x', rotation=45)

plt.show()


fig2, ax2 = plt.subplots(2, 2, figsize=(15, 12))
fig2.suptitle("Crime Data Analysis - Part 2", fontsize=16)
fig2.subplots_adjust(hspace=0.4)

# 5. Overall Crime Distribution (Pie Chart)
ax2[0, 0].pie(total_crimes, labels=total_crimes.index, autopct='%1.1f%%')
ax2[0, 0].set_title('5. Overall Crime Distribution')

# 6. Year-wise All Crime Trends
for crime in crime_cols:
    ax2[0, 1].plot(yearly_crimes.index, yearly_crimes[crime], label=crime)
ax2[0, 1].set_title('6. Year-wise Crime Trends')
ax2[0, 1].set_xlabel('Year')
ax2[0, 1].set_ylabel('Cases')
ax2[0, 1].legend()

# 7. State-wise Crime Distribution (Grouped Bar)
state_crimes.plot(kind='bar', stacked=False, ax=ax2[1, 0]) 
ax2[1, 0].set_title('7. State-wise Crime Distribution')
ax2[1, 0].set_xlabel('State')
ax2[1, 0].set_ylabel('Total Crimes')
ax2[1, 0].tick_params(axis='x', rotation=45)

# 8. Year vs Rape Scatter Plot
ax2[1, 1].scatter(df['Year'], df['Rape'], color='red')
ax2[1, 1].set_title('8. Year vs Rape Cases')
ax2[1, 1].set_xlabel('Year')
ax2[1, 1].set_ylabel('Rape Cases')

plt.show()

fig3, ax3 = plt.subplots(1, 2, figsize=(15, 6))
fig3.suptitle("Crime Data Analysis - Part 3", fontsize=16)

# 9. Year-wise Total Crimes
ax3[0].plot(yearly_total.index, yearly_total.values, marker='o', color='green')
ax3[0].set_title('9. Year-wise Total Crimes')
ax3[0].set_xlabel('Year')
ax3[0].set_ylabel('Total Crimes')

# 10. Top 10 States by Total Crimes
ax3[1].bar(state_total.index, state_total.values, color='teal')
ax3[1].set_title('10. Top 10 States by Total Crimes')
ax3[1].set_xlabel('State')
ax3[1].set_ylabel('Total Crimes')
ax3[1].tick_params(axis='x', rotation=45)

plt.show()

# Modified last query: Getting overall top 5 states by calculating row sum
top = df.groupby("State")[crime_cols].sum().sum(axis=1).sort_values(ascending=False) 
print("\n--- Top 5 States by Total Crimes ---")
print(top.head(5))

unique_values = df["State"].unique()
print(unique_values)