#!/usr/bin/env python
# coding: utf-8

# Copyright Jana Schaich Borg/Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)

# # How to Meet and Retrieve Your Data

# Watershed's intern put together a couple of sources of information that will be useful for your project. These three types of information are contained in the capstone database:
# 1. the current monthly rent Watershed charges for all of their client’s 244 properties, as well as the property type and geographic location of those properties. 
# 2. some general information about examples of short-term rental properties.  This information can be used to get a sense of what kind of nightly rental price Watershed’s client’s properties *could* be listed for, if they were converted to short-term rentals.
# 3. records about when those short-term rental properties were rented out, so that you can calculate their occupancy rates.  

# Your job is to determine how the database is organized so that you can retrieve all of the available information about Watershed’s client’s 244 properties, as well as the corresponding short-term rental information for comparable properties in the same location and of the same type.
# 1. Start by determining what tables the database contains, and what fields are included in each table.  
# 2. Then, we recommend that you make at least a rough relational schema of how the database is organized, so that you know what fields you can use to join tables. 
# 3. Next, make a list of the columns of data you want to retrieve in your final output.  
# 4. Finally, write your query to retrieve the desired data from the database.  

# Here are some hints about how to write your query:
# * Start by joining no more than two tables.  After you have made sure the query works as written and that the output makes sense, add other tables one at a time, checking the new query and its results each time.
# * Your final output should have 244 rows.  Given the limited output, the easiest way to extract the results will be to copy and paste the output from your query into Excel, although you could also extract as a .csv file and open that with Excel.  If you choose the .csv option, you might find it necessary to write your query on multiple lines when you declare it as a variable.  To do this, type a space (if you forget the space the lines will run together) and a "\" at the end of each line of your query:
# 
# ```
# my_data= %sql SELECT DISTINCT user_guid, state, membership_type \
# FROM users \
# WHERE country="US" AND state IS NOT NULL and membership_type IS NOT NULL \
# ORDER BY state ASC, membership_type ASC ;
# 
# my_data.csv('my_data.csv')
# ```
# 
# * We recommend that you calculate the occupancy rates of the example short-term rental properties within MySQL, rather than within Excel (it will be much faster!)  To do this, only examine rental dates during 2015, and remember that there are 365 days in the year.  The final output of your calculation should be the percentage of days in 2015 that the property was occupied.  You may want to consider using a subquery for this calculation.
# * Make sure that you extract information from short-term rentals <u>**_that have the same location and property type_**</u> as the 244 Watershed properties.
# * If you run into trouble, use your workbooks and Teradata notes from “Managing Big Data with MySQL” to remind you how to implement different parts of your query.
# 
# <img src="https://duke.box.com/shared/static/svbdzasxe7nncnszps6ewnkr8og4798c.jpg" width="300" alt="SQL Master"/>

# ## Good luck and have fun!

# To get started, connect to the capstone database and set the database as your default database using the following commands:
# 
# ```python
# %load_ext sql
# %sql mysql://studentuser:studentpw@localhost/capstone 
# %sql USE capstone
# ```

# ### Load and connect to the database

# In[8]:


get_ipython().run_line_magic('load_ext', 'sql')
get_ipython().run_line_magic('sql', 'mysql://studentuser:studentpw@localhost/capstone')
get_ipython().run_line_magic('sql', 'USE capstone')


# ### Queries
# 
# You can add as many "cells" as you need in order to explore the database and extract the appropriate data.  For a reminder about what "cells" are, how to add them, or how to use Jupyter in general, please refer to the "How to Use Jupyter Notebooks" video at: https://www.coursera.org/learn/analytics-mysql/lecture/oxkUg/how-to-use-jupyter-notebooks.

# In[6]:


get_ipython().run_cell_magic('sql', '', 'SHOW TABLES;')


# In[7]:


get_ipython().run_cell_magic('sql', '', 'DESC location')


# In[9]:


get_ipython().run_cell_magic('sql', '', 'SELECT *\nFROM location\nLIMIT 10;')


# In[4]:


get_ipython().run_cell_magic('sql', '', 'DESC property_type;')


# In[14]:


get_ipython().run_cell_magic('sql', '', 'SELECT *\nFROM property_type\nLIMIT 10;')


# In[6]:


get_ipython().run_cell_magic('sql', '', 'DESC st_property_info;')


# In[7]:


get_ipython().run_cell_magic('sql', '', 'SELECT *\nFROM st_property_info\nLIMIT 10;')


# In[8]:


get_ipython().run_cell_magic('sql', '', 'DESC st_rental_dates;')


# In[9]:


get_ipython().run_cell_magic('sql', '', 'SELECT *\nFROM st_rental_dates\nLIMIT 10;')


# In[10]:


get_ipython().run_cell_magic('sql', '', 'DESC st_rental_prices;')


# In[11]:


get_ipython().run_cell_magic('sql', '', 'SELECT *\nFROM st_rental_prices\nLIMIT 10;')


# In[12]:


get_ipython().run_cell_magic('sql', '', 'DESC watershed_property_info;')


# In[14]:


get_ipython().run_cell_magic('sql', '', 'SELECT *\nFROM watershed_property_info\nLIMIT 10;')


# In[19]:


get_ipython().run_cell_magic('sql', '', 'SELECT wpi.ws_property_id, loc.location_id, loc.city, loc.state, loc.zipcode, pt.apt_house, pt.num_bedrooms, pt.kitchen, pt.shared, wpi.current_monthly_rent, strp.percentile_10th_price, strp.percentile_90th_price, strp.sample_nightly_rent_price\nFROM watershed_property_info wpi\n\nJOIN location loc\nON wpi.location = loc.location_id\n\nJOIN st_rental_prices strp\nON loc.location_id = strp.location\n\nJOIN property_type pt\nON strp.property_type = pt.property_type_id\n\nORDER BY ws_property_id')


# In[21]:


get_ipython().run_cell_magic('sql', '', 'SELECT DISTINCT w.ws_property_id,w.location, w.property_type,w.current_monthly_rent,srp.percentile_10th_price,srp.percentile_90th_price,srp.sample_nightly_rent_price,srd.rental_date,srd.st_property, COUNT(srd.rental_date)/365 AS occupancy_rate,p.apt_house,p.num_bedrooms,p.kitchen,p.shared,l.city,l.state,l.zipcode \nFROM watershed_property_info w \nJOIN st_property_info spi \nON (w.location=spi.location AND w.property_type=spi.property_type) \nJOIN st_rental_prices srp \nON (spi.location=srp.location AND spi.property_type=srp.property_type) \nJOIN property_type p \nON w.property_type=p.property_type_id \nJOIN location l \nON w.location=l.location_id \nJOIN st_rental_dates srd \nON spi.st_property_id = srd.st_property \nWHERE YEAR(srd.rental_date)=2015 GROUP BY srd.st_property  ')


# In[ ]:




