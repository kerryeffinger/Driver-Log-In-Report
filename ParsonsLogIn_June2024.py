#!/usr/bin/env python
# coding: utf-8

# ## ***AVL Log In Report***  
# ### **Weekly report with District, Subdistrict, Management Unit (Garage) with percent logged in vs. not**  
# ### **June 2024 with updated columns from Parsons**
# ### Date: January 10, 2024  

# #### Updates: January 25, 2024
# #### March 5, 2024: made change to df4, was calculated based on df2 when it should have been df3  
# #### June 26, 2024: csv file format and column names/order changed, so need to update notebook
# #### Aug. 20, 2024: updated sub_lookup with 7 additional garages (units still not matching between INDOT and Parsons, but they are mapped to correct subs) and changed join to left join so un-matched units/subs will be called out in the final output

# In[2]:


import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[4]:


#import glob
#import os
#from pathlib import Path


# ### **Concatenating several .csv files, ignore_index = TRUE***

# In[7]:


df1 = pd.read_csv('Log_In_10_28_24.csv')
df2 = pd.read_csv('Log_In_10_29_24.csv')
df3 = pd.read_csv('Log_In_10_30_24.csv')
df4 = pd.read_csv('Log_In_10_31_24.csv')
df5 = pd.read_csv('Log_In_11_1_24.csv')
df6 = pd.read_csv('Log_In_11_2_24.csv')
df7 = pd.read_csv('Log_In_11_3_24.csv')


# In[9]:


file2 = pd.concat([df1, df2, df3, df4, df5, df6, df7], 
                  ignore_index = True)


# In[11]:


file2.sample(5)


# In[13]:


#file2.drop('Unnamed: 7', inplace=True, axis=1)
#changed for updated columns 6/24


# In[15]:


file2.columns


# In[17]:


#garage2 = pd.DataFrame(file2['Garage'].unique())


# ### **Loading Sub Lookup Table, to add column for subdistricts to data from Parsons**  
# Double check number of rows of subs with columns of df below

# In[20]:


sub = pd.read_csv("sub_lookup_table.csv")
sub


# ### **Combining data from Parsons (for several days) with Sub lookup then reordering columns**

# In[23]:


df = file2.merge(sub, how= 'left')


# In[25]:


df


# In[27]:


df.columns


# In[29]:


column_names = ['Date', 'District', 'Subdistrict', 'Garage', 'Truck', 'Operator Name', 'Total Hours',
       'Total Miles', 'Login Time', 'Logoff Time']
#changed 6/24


# In[31]:


df2 = pd.DataFrame(df, columns = column_names)
df2.head(5)


# In[33]:


df2 = df2.sort_values( by = ['District', 'Subdistrict'])


# In[35]:


df2_Cr = df2[df2['District'] == 'Crawfordsville']
df2_Cr.head(3)


# In[37]:


df2_Fo = df2[df2['District'] == 'Fort Wayne']
df2_Fo.head(3)


# In[39]:


df2_Gr = df2[df2['District'] == 'Greenfield']
df2_Gr.head(3)


# In[41]:


df2_La = df2[df2['District'] == 'LaPorte']
df2_La.head(3)


# In[43]:


df2_Se = df2[df2['District'] == 'Seymour']
df2_Se.head(3)


# In[45]:


df2_Vi = df2[df2['District'] == 'Vincennes']
df2_Vi.head(3)


# In[47]:


dist = pd.read_csv('sub_dist_lookup_table.csv')
dist


# ### **Unknown Analysis with ALL DATA (not filtered for less than 10 miles):**

# In[50]:


unknown = df2[df2["Operator Name"] == "Unknown"]
unknown.sample(3)
#changed 6/24


# In[52]:


number_unknown = len(unknown.index)


# In[54]:


number_unknown


# In[56]:


n_unknown = unknown['Operator Name'].groupby(unknown.Garage).count()
n_unknown_df = pd.DataFrame(n_unknown)
n_unknown_df.rename(columns={'Operator Name':'number_unknown'}, inplace=True)
n_unknown_df['total_trucks'] = df2['Operator Name'].groupby(df2.Garage).count()
n_unknown_df['percent_unknown'] = n_unknown_df['number_unknown']/n_unknown_df['total_trucks']
n_unknown_df['percent_logged_in'] = 1 - n_unknown_df['percent_unknown']
n_unknown_df['number_logged_in'] = n_unknown_df['total_trucks'] - n_unknown_df['number_unknown']


# In[58]:


n_unknown_df


# In[60]:


n_unknown_df.columns


# In[62]:


column_names2 = ['number_logged_in','number_unknown', 'total_trucks',
       'percent_logged_in', 'percent_unknown']


# In[64]:


unknown_df = pd.DataFrame(n_unknown_df, columns = column_names2)


# In[66]:


unknown_df.reset_index()


# In[68]:


unknown_df2 = unknown_df.merge(sub, how = "left", on = "Garage")


# In[70]:


unknown_df2


# In[72]:


unknown_df2 = unknown_df2.merge(dist, how = "left", on = "Subdistrict")
unknown_df2


# In[74]:


column_names3 = ['District','Subdistrict','Garage', 'number_logged_in', 'number_unknown', 'total_trucks',
       'percent_logged_in', 'percent_unknown']


# In[76]:


unknown_df3 = pd.DataFrame(unknown_df2, columns = column_names3)


# In[78]:


unknown_df3 = unknown_df3.sort_values( by = ['Subdistrict', 'Garage'])
#Subdistrict and Garage breakdown


# In[80]:


unknown_df3


# ## **Same analysis but remove rows with less than 10 miles**

# In[83]:


#df2['Total Miles'] = pd.to_numeric(df2['Total Miles'])


# In[85]:


df3 = df2.drop(df2[df2['Total Miles'] <= 10].index)


# In[87]:


df3 = df3.sort_values( by = ['District', 'Subdistrict'])


# In[89]:


df3


# In[91]:


unknown2 = df3[df3["Operator Name"] == "Unknown"]
unknown2
#changed 6/24


# In[93]:


#unknown2


# In[95]:


#create df with number and percent unknown operators
n_unknown2 = unknown2['Operator Name'].groupby(unknown2.Garage).count()
df4 = pd.DataFrame(n_unknown2)
df4.rename(columns={'Operator Name':'number_unknown'}, inplace=True)
df4['total_trucks'] = df3['Operator Name'].groupby(df3.Garage).count()
df4['percent_unknown'] = df4['number_unknown']/df4['total_trucks']
df4['percent_logged_in'] = 1 - df4['percent_unknown']
df4['number_logged_in'] = df4['total_trucks'] - df4['number_unknown']


# #### Next, reorder columns, reset index, then merge with sub df

# In[98]:


column_names4 = ['number_logged_in','number_unknown', 'total_trucks',
       'percent_logged_in', 'percent_unknown']


# In[100]:


unknown_df4 = pd.DataFrame(df4, columns = column_names4)
unknown_df4.reset_index()


# In[102]:


unknown_df5 = unknown_df4.merge(sub, how = "left", on = "Garage")


# In[104]:


unknown_df5 = unknown_df5.merge(dist, how = "left", on = "Subdistrict")
unknown_df5


# ### reorder columns again, then sort by sub and garage (and District!1 which was added 9/30/24)

# In[107]:


unknown_df5.columns


# In[109]:


column_names5 = ['District','Subdistrict', 'Garage', 'number_logged_in', 'number_unknown', 'total_trucks',
       'percent_logged_in', 'percent_unknown']
unknown_df6 = pd.DataFrame(unknown_df5, columns = column_names5)


# In[111]:


unknown_df6 = unknown_df6.sort_values( by = ['Subdistrict', 'Garage'])


# In[113]:


unknown_df6


# In[115]:


unknown_df_Cr = unknown_df6[unknown_df6['District'] == 'Crawfordsville']
unknown_df_Cr


# In[117]:


unknown_df_Fo = unknown_df6[unknown_df6['District'] == 'Fort Wayne']
unknown_df_Fo


# In[119]:


unknown_df_Gr = unknown_df6[unknown_df6['District'] == 'Greenfield']
unknown_df_Gr


# In[121]:


unknown_df_La = unknown_df6[unknown_df6['District'] == 'LaPorte']
unknown_df_La


# In[123]:


unknown_df_Se = unknown_df6[unknown_df6['District'] == 'Seymour']
unknown_df_Se


# In[125]:


unknown_df_Vi = unknown_df6[unknown_df6['District'] == 'Vincennes']
unknown_df_Vi


# ## **Plots:**

# In[128]:


unknown_df3_plot = unknown_df3[['Subdistrict','Garage','percent_unknown']]
unknown_df3_plot = unknown_df3_plot.set_index('Subdistrict')


# In[130]:


unknown_df3_plot


# In[132]:


unknown_df3_plot.plot.barh()
plt.title('Percent Unknown Operators by Subdistrict and Garager')
plt.xlabel('')


# ## **Save dfs to Excel file**

# In[135]:


unknown_df3.sample(3)


# In[137]:


with pd.ExcelWriter('Operators_Logged_In_11_04_24_Indiana.xlsx') as writer:
    df2.to_excel(writer, sheet_name = 'All Data for Week')
    unknown_df3.to_excel(writer, sheet_name = '# Unknown All Data')
    df3.to_excel(writer, sheet_name = 'Data More than 10 Miles')
    unknown_df6.to_excel(writer, sheet_name = '# Unknown > 10 Miles')


# In[280]:


#df2.to_excel("03_08_2024_All_Log_Ins_with_subs.xlsx")


# ### Crawfordsville Excel File

# In[139]:


with pd.ExcelWriter('Craw_Operators_Logged_In_11_04_24.xlsx') as writer:
    df2_Cr.to_excel(writer, sheet_name = 'All Data for Week')
    unknown_df_Cr.to_excel(writer, sheet_name = '# Unknown > 10 Miles')


# ### Fort Wayne Excel File

# In[141]:


with pd.ExcelWriter('Fort_Operators_Logged_In_11_04_24.xlsx') as writer:
    df2_Fo.to_excel(writer, sheet_name = 'All Data for Week')
    unknown_df_Fo.to_excel(writer, sheet_name = '# Unknown > 10 Miles')


# ### Greenfield Excel File

# In[143]:


with pd.ExcelWriter('Gree_Operators_Logged_In_11_04_24.xlsx') as writer:
    df2_Gr.to_excel(writer, sheet_name = 'All Data for Week')
    unknown_df_Gr.to_excel(writer, sheet_name = '# Unknown > 10 Miles')


# ### LaPorte Excel File

# In[145]:


with pd.ExcelWriter('Lapo_Operators_Logged_In_11_04_24.xlsx') as writer:
    df2_La.to_excel(writer, sheet_name = 'All Data for Week')
    unknown_df_La.to_excel(writer, sheet_name = '# Unknown > 10 Miles')


# ### Seymour Excel File

# In[147]:


with pd.ExcelWriter('Seym_Operators_Logged_In_11_04_24.xlsx') as writer:
    df2_Se.to_excel(writer, sheet_name = 'All Data for Week')
    unknown_df_Se.to_excel(writer, sheet_name = '# Unknown > 10 Miles')


# ### Vincennes Excel File

# In[149]:


with pd.ExcelWriter('Vinc_Operators_Logged_In_11_04_24.xlsx') as writer:
    df2_Vi.to_excel(writer, sheet_name = 'All Data for Week')
    unknown_df_Vi.to_excel(writer, sheet_name = '# Unknown > 10 Miles')


# In[ ]:




