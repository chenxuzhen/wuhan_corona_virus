import sys
import pandas as pd
import re
# from IPython.core.interactiveshell import InteractiveShell
# InteractiveShell.ast_node_interactivity = "all"
# 中文乱码csv输出：（encoding='utf-8') > encoding='utf_8_sig'

import xlrd

input_file1 = r'C:\Users\xuzhen\国家中英文对照表.csv'
input_file2 = r'C:\Users\xuzhen\世界各国中英文对照.xlsx'

df = pd.read_csv(input_file1)
print("df1 before - csv") 
df

def clean_name(df, column):
    
    df[column] = df[column].str.replace('(', ' ')
    df[column] = df[column].str.replace(')', '')
    df[column] = df[column].str.replace(',','')
    df[column] = df[column].str.replace(':','')


clean_name(df, 'country1')
clean_name(df, 'country2')
clean_name(df, 'abbrev')
print("df1 updated - csv")        
df
df.to_csv("国家中英文对照表_clean_name.csv",encoding='utf_8_sig')

df2 = pd.read_excel(input_file2, 'Sheet1')
print("df2 before - excel")        
df2

for worksheet_name in df2.items():
    if re.search('\(*', str(df2['中文'])): 
        

        # Extract the position of beginning of pattern 
        pos = re.search('\(*', str(df2['中文'])).start() 
        print((df2['中文'])[:pos])
        # return the cleaned name 
        df2['中文'] = (df2['中文'])[pos:] 
print("df2 is updated:")
df2
df2.to_excel("世界各国中英文对照_clean_name.xlsx")

# print(df2['英文'])
# print(df2['中文'])

# clean_name(df2, '英文')
# clean_name(df2, '中文')
# print(df2)
    
    
# df['country1'] = df['country1'].str.replace('(', '').replace(')', '')
# df['country1'] = df['country1'].str.replace(')', '')

# df['country2'] = df['country2'].str.replace(':', '')
# df['abbrev'] = df['abbrev'].str.replace(',', '')
  
# # Function to clean the names 
# def Clean_names(City_name): 
    # # Search for opening bracket in the name followed by 
    # # any characters repeated any number of times 
    # if re.search('\(.*', City_name): 
  
        # # Extract the position of beginning of pattern 
        # pos = re.search('\(.*', City_name).start() 
  
        # # return the cleaned name 
        # return City_name[:pos] 
  
    # else: 
        # # if clean up needed return the same name 
        # return City_name 
          
# # Updated the city columns 
# df = df.apply(Clean_names) 
  
# Print the updated dataframe 
#print(df) 
