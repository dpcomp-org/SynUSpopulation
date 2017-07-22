# Lets find the warning
# short script
import pandas as pd

mymap={3:1, 5:4, 2:2, 1:8}

print("test 1: Define dataframe, call map")
df1=pd.DataFrame([[3,5],[5,5],[2,5],[1,6]], columns=['a','b'])
df1['a']=df1['a'].map(mymap)
print("No warning")

print("test 2: Define dataframe, slice dataframe, call map")
df2=pd.DataFrame([[3,5],[5,5],[2,5],[1,6]], columns=['a','b'])
df2=df2[df2['b']==5]
df2['a']=df2['a'].map(mymap)
print("No warning")

print("test 3: Define dataframe, define function with mapping, call function")
df3=pd.DataFrame([[3,5],[5,5],[2,5],[1,6]], columns=['a','b'])

def foo1(df,mymap):
    df['a']=df['a'].map(mymap)

foo1(df3, mymap)
print("No warning")

print("test 4: Define dataframe, define function with slicing and mapping, call function")
df4=pd.DataFrame([[3,5],[5,5],[2,5],[1,6]], columns=['a','b'])

def foo2(df,mymap): #df passed by reference
    df=df[df['b']==5] #local copy made
    df['a']=df['a'].map(mymap) #warning

foo2(df4, mymap) #first call
print("warning on first call")
foo2(df4, mymap) #must be surpressed on second call?
print("no warning on second call")

print("test 5: define new function that is same as previous one, call function")
def foo3(df,mymap):
    df=df[df['b']==5]
    df['a']=df['a'].map(mymap)

foo3(df4, mymap) #new function first call
print("warning")
foo2(df4, mymap)
