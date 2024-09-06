# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 12:50:18 2024

@author: falih
"""

import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt



data = pd.read_csv('fifa21_raw_data.csv')

data_cleaned = pd.read_csv('fifa21 raw data v2.csv') # to compare to already cleaned one


# split_col = data['Height'].str.split('', expand = True)

# splitting height column to find inches 

length = len(data['Height'])
inc = []
for x in range (0,length):
    y = data['Height'][x][2:-1]
    inc.append(y)

# splitting height column to find feet 

ft = []
for x in range (0,length):
    y = data['Height'][x][0:1]
    ft.append(y)

# change the columns into dataframes

dfinc = (pd.DataFrame(inc)).astype(int)

dfft = (pd.DataFrame(ft)).astype(int)

# converge the two columns into single column in cm

height_in_cm = []
for x in range(0,length):
    a = dfft.iloc[x,0]
    b = dfinc.iloc[x,0]
    cm1 = round(a * 30.48)
    cm2 = round(b * 2.54)
    y = cm1 + cm2
    height_in_cm.append(y)
    

data['height_cm'] = height_in_cm

# data = data.drop('Height', axis = 1)

# split column for adding comma in positions column

split_col = data['Positions'].str.split(' ',expand = True)

# add comma after each position

pos1 = split_col[0]
pos2 = split_col[1]
pos3 = split_col[2]

# column 0

pos_comma = []
for x in range (0,length):
    a = split_col[0][x]
    b = split_col[1][x]
    # c = split_col[2][x]
    # d = a + ', '
    # e = b + ', '
    # f = c + ', '
    try : 
        if b == None:
            y = a
        else:
            y = a+', '
    except:
        pass
    pos_comma.append(y)


# column 1
length = len(data['Positions'])
pos_2 = []
for x in range (0,length):
    a = split_col[1][x]
    # b = split_col[1][x]
    # c = split_col[2][x]
    # d = a + ', '
    # e = b + ', '
    # f = c + ', '
    # try :
    if split_col[2][x] == None:
       b = a
    elif split_col[2][x] != None:
       b =  a + ', '
    elif a == None:
       b =  ''
    # else : 
    #     pass 
    pos_2.append(b)
    
    
# cleaning column 1
length = len(data['Positions'])
pos_2clean = []
for x in range (0,length):
    a = pos_2[x]
    if a == None:
        b = ''
    else:
        b = a
    pos_2clean.append(b)
    
    
# cleaning column 2
length = len(data['Positions'])
pos_3= []
for x in range (0, length):
    a = split_col[2][x]
    if a == None:
        b = ''
    else:
        b = a
    pos_3.append(b)
        


# join all 3 columns
length = len(data['Positions'])
pos_joined = []
for x in range(0,length):
    a = pos_comma[x]
    b = pos_2clean[x]
    c = pos_3[x]
    z = a+b+c
    pos_joined.append(z)
    
# append cleaned column with previous column

data['Positions'] = pos_joined

# cleaning weight column

# splitting weight column to convert into str. format to slicing dataframe :

weight_split = (data['Weight'].str.slice(0,3)).astype(int)


length = len(data['Weight'])
in_kg = []
for x in range (0,length):
    y = weight_split[x]
    z = round(y * 0.453592)
    in_kg.append(z)

# append into Weight column in the dataframe

data['Weight_in_kg'] = in_kg

# flag players who have been in the club for 10 years

d = datetime.datetime(2021,2,14)

length = len(data['Joined'])
today = []
for x in range(0,length):
    e = d.strftime('%Y-%m-%d')
    today.append(d)
    

# change datetime format to generate the flagged column

length = len(data['Joined'])
flagged = []
for x in range(0,length):
    y = data['Joined'][x]
    z = datetime.datetime.strptime(y, '%b %d, %Y')
    a = z.strftime('%Y-%m-%d')
    flagged.append(a)

# find date differences for each row in the flagged column
# change the string into UNIX time to find date differences

# abs((d2-d1).year)
# abs((d2-d1).days)

joined_unix = []
for x in range (0,length):
    f = flagged[x]
    g = today[x]
    h = datetime.datetime.strptime(f,'%Y-%m-%d')
    joined_unix.append(h)
    
# find date differences

length = len(data['Joined'])
date_diff = []
date_differences = []
ten_flag = []   
for x in range(0,length):
    a = today[x]
    b = joined_unix[x]
    c = abs((a - b).days)
    date_diff.append(c)
    d = round(date_diff[x] / 365 ,1)
    date_differences.append(d)
    if date_differences[x] >= 10:
        e = 1
    else:
        e = 0
    ten_flag.append(e)

# append the column into dataframe
data['stay10years'] = ten_flag


# find count of players who have been in the same club for > 10 years

tenyears = data.groupby(['stay10years'])['ID'].count()

num_players = data.groupby(['foot'])['ID'].count()

# cleaning and transform wage column (slicing, removing '' values)

# creating bar chart 

num_players.plot.bar()
plt.show()


length = len(data['Wage'])
wage = []
wage_cleaned = []
wage_cleaned1 = []
for x in range (0, length):
    y = data['Wage'][x][1:]
    wage.append(y)
    z = wage[x][:-1]
    wage_cleaned.append(z)
    a = wage_cleaned[x]
    if a == '':
        b = '0'
    else:
        b = a
    wage_cleaned1.append(b)
        
# change the column datatype into dataframe integer
df_wage = (pd.DataFrame(wage_cleaned1)).astype(int)

data['Wage_cln'] = df_wage

# converting K to M 

length= len(data['Wage'])
wage_in_M = []
for x in range(0,length):
    y = df_wage.iloc[x,0]
    z = y / 1000
    wage_in_M.append(z)

data['Wage_in_M'] = wage_in_M

# cleaning and transform value column (slicing, removing '' values)

length = len(data['Value'])
value = []
value_c = []
value_cleaned = []
for x in range (0,length):
    y = data['Value'][x][1:]
    value.append(y)
    z = value[x][:-1]
    value_c.append(z)
    a = value_c[x]
    if a == '':
        b = '0'
    else:
        b = a
    value_cleaned.append(b)

# change value_cleaned column into pandas dataframe so it can be converted as int/float

df_value = (pd.DataFrame(value_cleaned)).astype(float)

data['Value_cleaned'] = df_value

# creating scatterplot chart using matplotlib

xpoint = data['Wage_cln']
ypoint = data['Value_cleaned'] 
plt.scatter(xpoint,ypoint, color = 'red')
plt.show() # so many players are underpaid hence their values


