#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


# In[3]:


## make sure you install either the chrome driver or mozilla driver and place .exe file in the PATH environment variable


# In[4]:


driver = webdriver.Chrome()

driver.get(url="https://www.imax.com/theatres")

assert "Theatres" in driver.title ## test that the correct web page is loaded before we proceed

elem = driver.find_element_by_id("edit-street-address") #find the input form


# In[5]:


## read excel file for county names
## for fact check, add up the population numbers and see if it's around 330m (it is)

## make sure the path to the excel file is correct
county_df = pd.read_excel('./county_population.xlsx')
county_df.head()
county_list = county_df['GEO.display-label'].tolist()


# In[ ]:





# In[6]:


county_list = county_list[1:]
county_list


# In[12]:


#create empty theatre dataframe with 4 columns

theatre_col = ["Address", "City", "State", "Zip Code"]
theatre_df = pd.DataFrame(columns = theatre_col)


# In[ ]:





# In[14]:


# use a try/except in the forloop to ignore any errors that come up
# in the loop, the program will clear the input, type in the county name, press enter, wait 6 seconds, get the addresses from the 
# DOM, format the DOM element to a pandas dataframe, and then concat the DOM element (now dataframe) to the theatre dataframe

## You can split the work into batches:
## Run multiple instances of this script and split the county list into multiple batches to work on in parallel
## The scripts should open separate webdrivers/browsers and start iterating over their own segments of the list.
## Any overlap in addresses can be dropped after the fact.
## After the scripts are finished, you can consolidate the data in excel or python. I used excel.

for county in county_list: 
    try:
        print(county_list.index(county))
        elem.clear() #clear the input form
        elem.send_keys(county)  #type into the input form our address
        elem.send_keys(Keys.RETURN) #submit the form
        time.sleep(6) ## need sleep time to wait for the response from IMAX's servers. The time may vary depending on your internet 
                      ## speed, but I felt like this was the best way to do it for now, since I have limited time.
                      
        address = driver.find_elements_by_class_name("theatre-address") # list of theatre addresses

        # need to make sure the webpage has loaded and is not empty
        # assert that the exception message is not present

        for i in address:
            print(i.text)
            if i.text == "": ## some fields are empty, so we will ignore them and move on to the next field or county
                continue
            ## split each theatre address into 4 columns
            res = i.text.split(',')
            res.append(res[-1][-5:])
            res[-2] = res[-2][1:3]
            res[:-3] = [''.join(res[:-3])]
            print(res)
            ## res is now a list of 4 items, corresponding to the dataframe columns
            ## convert the res list to a dataframe to add to our existing dataframe
            df =pd.DataFrame([res], columns=theatre_df.columns)
            theatre_df = pd.concat([theatre_df, df], ignore_index=True) ## set ignore_index to True for the row indexes of
                                                                        ## theatre_df to correspond to a row's row number
            # drop_duplicates() returns a df with all dups dropped. set the returned df to theatre_df
            theatre_df = theatre_df.drop_duplicates() 
    except Exception:
        #here we ignore any errors and move on
        pass



# In[15]:


theatre_df


# In[16]:


# if you are running batches, save the batches to different excel files and then add them up manually
writer = pd.ExcelWriter('firstChunk.xlsx')
theatre_df.to_excel(writer, 'sheet1')
writer.save()


# In[ ]:




